document$.subscribe(function () {
    function handleRepoInfo() {
        // The last <a class="repo"> element
        var $lastRepoLink = $("a.repo").last();
        if ($lastRepoLink.length === 0) {
            $(".md-header__source").css("display", "none");
            $(".md-source__facts").css("display", "none");
            $(".md-md-source__fact--stars").css("display", "none");
            $(".md-md-source__fact--forks").css("display", "none");
            $(".md-md-source__fact--version").css("display", "none");
            $(".md-source").attr("href", "");
        } else {
            var repoName = $.trim($lastRepoLink.text());
            var repoLink = $lastRepoLink.attr("href");

            var match = repoLink.match(
                /^https:\/\/github\.com\/([^/]+)\/([^/]+)\/?$/i
            );
            if (match) {
                var owner = match[1];
                var repo = match[2];
                if (!repoName) {
                    repoName = `${owner}/${repo}`;
                }

                // If the repo info is already set, don't fetch it again
                if ($(".md-source").attr("href") === repoLink) {
                    return;
                }

                $(".md-source__repository")
                    .contents()
                    .filter(function () {
                        return this.nodeType === 3; // Node.TEXT_NODE
                    })
                    .first()
                    .replaceWith(repoName);
                $(".md-source").attr("href", repoLink);
                $(".md-header__source").css("display", "block");

                var repoInfoDeferred = $.Deferred();
                var latestReleaseDeferred = $.Deferred();

                // Basic repo info
                $.ajax({
                    url: `https://api.github.com/repos/${owner}/${repo}`,
                    method: "GET",
                    success: function (repoData) {
                        repoInfoDeferred.resolve(repoData);
                    },
                    error: function () {
                        console.error(
                            "Failed to fetch repo info for " + repoLink
                        );
                        repoInfoDeferred.resolve(null); // Resolve with null on error
                    },
                });

                // Latest release info
                $.ajax({
                    url: `https://api.github.com/repos/${owner}/${repo}/releases/latest`,
                    method: "GET",
                    success: function (releaseData) {
                        latestReleaseDeferred.resolve(releaseData);
                    },
                    error: function () {
                        console.error(
                            "Failed to fetch latest release for " + repoLink
                        );
                        latestReleaseDeferred.resolve(null); // Resolve with null on error
                    },
                });

                // When all requests are done
                $.when(repoInfoDeferred, latestReleaseDeferred).done(function (
                    repoData,
                    releaseData
                ) {
                    if (repoData || releaseData) {
                        $(".md-source__facts").css("display", "flex");
                    }

                    if (repoData) {
                        $(".md-source__fact--stars")
                            .text(`${repoData.stargazers_count}`)
                            .css("display", "list-item");
                        $(".md-source__fact--forks")
                            .text(`${repoData.forks_count}`)
                            .css("display", "list-item");
                    }

                    if (releaseData) {
                        $(".md-source__fact--version")
                            .text(`${releaseData.tag_name}`)
                            .css("display", "list-item");
                    }
                });
            } else {
                $(".md-header__source").css("display", "none");
                $(".md-source__facts").css("display", "none");
                $(".md-md-source__fact--stars").css("display", "none");
                $(".md-md-source__fact--forks").css("display", "none");
                $(".md-md-source__fact--version").css("display", "none");
                $(".md-source").attr("href", "");
                console.error("Invalid GitHub repository link: " + repoLink);
            }
        }
    }
    handleRepoInfo();
});

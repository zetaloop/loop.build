(function () {
    function replaceUrl(str, targetPath) {
        const regex = new RegExp(
            `(https?):\\/\\/loop\\.build(:\\d+)?\\/${targetPath}\\/`,
            "g"
        );
        return regex.test(str)
            ? str.replace(regex, function (match, protocol, port) {
                  return `${protocol}://docs.loop.build${port || ""}/`;
              })
            : null;
    }
    (function (history) {
        var pushState = history.pushState;

        history.pushState = function (state, title, url) {
            if (url && url instanceof URL) {
                // console.log("pushState called with URL:", url.href);
                var redirectList = ["docs", "tools", "blog", "update", "about"];
                for (var i = 0; i < redirectList.length; i++) {
                    newUrl = replaceUrl(url.href, redirectList[i]);
                    if (newUrl) {
                        url.href = newUrl;
                        window.location.href = url;
                        return;
                    }
                }
            }
            return pushState.call(history, state, title, url);
        };
    })(window.history);
})();

// Hook theme change event, fix the mess.

document$.subscribe(function () {
    var lastScheme = document.body.getAttribute("data-md-color-scheme");
    var lastPrimary = document.body.getAttribute("data-md-color-primary");
    // var lock = false;

    var observer = new MutationObserver(function (mutations) {
        // if (lock) return;
        mutations.forEach(function (mutation) {
            if (mutation.attributeName === "data-md-color-scheme") {
                newScheme = document.body.getAttribute("data-md-color-scheme");
                newPrimary = document.body.getAttribute(
                    "data-md-color-primary"
                );
                if (lastScheme == newScheme) return;

                /*console.log("Detected data-md-color-scheme change:", newScheme);
                var elements = Array.from(
                    eval(
                        'document.querySelectorAll(".highlighttable, code, .md-typeset__table, .mermaid, .md-header-bg")'
                    ) // If you dont use eval, mermaid will not be detected
                );
                var filteredElements = elements.filter(function (el) {
                    // Check if the element is not a child of another element in the list
                    return !elements.some(function (parent) {
                        return parent !== el && parent.contains(el);
                    });
                });

                filteredElements.forEach(function (el) {
                    try {
                        el.classList.remove("theme-changed");
                        void el.offsetWidth;
                        el.classList.add("theme-changed");
                        // console.log("Fixed theme for element:", el);
                    } catch (e) {}
                });*/

                // lock = true;
                // document.body.setAttribute("data-md-color-scheme", lastScheme);
                // document.body.setAttribute(
                //     "data-md-color-primary",
                //     lastPrimary
                // );
                // setTimeout(() => {
                //     document.body.setAttribute(
                //         "data-md-color-scheme",
                //         newScheme
                //     );
                //     document.body.setAttribute(
                //         "data-md-color-primary",
                //         newPrimary
                //     );
                //     lock = false;
                //     setTimeout(() => {
                //         $html.removeClass("theme-filter");
                //     }, 1);
                // }, 300);

                document.body.style.backgroundColor = getComputedStyle(
                    document.body
                ).getPropertyValue("--md-default-bg-color");

                $container = $(".md-content");
                $container.removeClass("theme-changed");
                $container.css("opacity", 0);
                setTimeout(() => {
                    $container.addClass("theme-changed");
                    $container.css("opacity", "");
                }, 0);

                $header = $(".md-header");
                $headerBg = $(".md-header-bg");
                $headerTabs = $(".md-tabs");
                $sidebar = $(".md-sidebar");
                $header.removeClass("theme-changed-fast");
                $headerBg.removeClass("theme-changed-fast");
                $headerTabs.removeClass("theme-changed-fast");
                $sidebar.removeClass("theme-changed-fast");
                $header.css("opacity", 0);
                $headerBg.css("opacity", 0);
                $headerTabs.css("opacity", 0);
                $sidebar.css("opacity", 0);
                setTimeout(() => {
                    $header.addClass("theme-changed-fast");
                    $headerBg.addClass("theme-changed-fast");
                    $headerTabs.addClass("theme-changed-fast");
                    $sidebar.addClass("theme-changed-fast");
                    $header.css("opacity", "");
                    $headerBg.css("opacity", "");
                    $headerTabs.css("opacity", "");
                    $sidebar.css("opacity", "");
                }, 0);

                lastScheme = newScheme;
                lastPrimary = newPrimary;
            }
        });
    });

    observer.observe(document.body, {
        attributes: true,
        attributeFilter: ["data-md-color-scheme"],
    });

    document.body.style.backgroundColor = getComputedStyle(
        document.body
    ).getPropertyValue("--md-default-bg-color");
});

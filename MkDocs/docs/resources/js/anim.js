// Hook theme change event, fix the mess.

document$.subscribe(function () {
    if (window.pageObserver) {
        window.pageObserver.disconnect();
    }
    var lastScheme = document.body.getAttribute("data-md-color-scheme");
    var lastPrimary = document.body.getAttribute("data-md-color-primary");

    function anim($el, cls) {
        $el.css("opacity", 0).removeClass(cls);
        setTimeout(() => {
            $el.css("opacity", "")
                .addClass(cls)
                .on("animationend", function () {
                    $el.removeClass(cls);
                });
        });
    }

    function handlePageAnim(force = false, mode = "full") {
        var newScheme = document.body.getAttribute("data-md-color-scheme");
        var newPrimary = document.body.getAttribute("data-md-color-primary");

        if (!force && lastScheme == newScheme) return;
        lastScheme = newScheme;
        lastPrimary = newPrimary;

        $container = $(".md-content");
        $header = $(".md-header");
        $headerBg = $(".md-header-bg");
        $headerBgFrame = $(".md-header-bg-frame");
        $headerTabs = $(".md-tabs");
        $sidebar = $(".md-sidebar");
        switch (mode) {
            case "init":
                anim(
                    $(
                        ".md-header__inner > *:not(.md-header__title):not(.md-logo)"
                    ),
                    "header-slidein"
                );
                anim($headerTabs, "header-slidein");
                anim($sidebar, "header-slidein");
                anim($container, "header-page-init");
                anim($headerBg, "header-bg-init");
                anim($headerBgFrame, "header-slidein");
                break;

            case "full":
                anim($container, "theme-changed");
                anim($sidebar, "theme-changed-fast");
                anim($header, "theme-changed-fast");
                anim($headerTabs, "theme-changed-fast");
                anim($headerBg, "theme-changed");
                break;

            case "page":
                anim($container, "page-changed");
                break;
        }
    }

    var observer = new MutationObserver(function (mutations) {
        mutations.forEach(function (mutation) {
            if (mutation.attributeName === "data-md-color-scheme") {
                handlePageAnim();
            }
        });
    });
    observer.observe(document.body, {
        attributes: true,
        attributeFilter: ["data-md-color-scheme"],
    });

    window.pageObserver = observer;
    window.pageAnim = handlePageAnim;
});

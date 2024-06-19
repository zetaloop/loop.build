document$.subscribe(() => {
    const $navHeader = $(".md-header");
    const $navTabs = $(".md-tabs");
    const $navContents = $(".md-tabs__list");
    var $navBackground = $(".md-header-bg");
    let lastScrollY = window.scrollY;

    // check handlers exist
    const isDuplicate = window.tabsEffectHandler !== undefined;

    function tabsEffectHandler() {
        const currentScrollY = window.scrollY;
        const navHeight = $navTabs.height();
        // navTabs.height == navHeader.height

        if (navHeight === 0) {
            console.error(
                "[tabsfix.js] navHeight is 0, md-tabs may not loaded yet."
            );
            return;
        }

        if ($navBackground.length === 0) {
            $navHeader.before(
                $(
                    '<div class="md-header-bg-frame">' +
                        '<div class="md-header-bg theme-changed-fast"></div>' +
                        "</div>"
                )
            );
            $navBackground = $(".md-header-bg");
        }

        if ($navTabs.css("display") === "none") {
            // Mobile view, ignore everything
            if ($navBackground.css("height") !== navHeight + "px") {
                $navBackground.css("height", navHeight + "px");
            }
            return;
        }

        if (currentScrollY > navHeight / 2) {
            // Y > navHeight/2 -> force hide
            if ($navContents.css("visibility") !== "collapse") {
                $navContents.css("visibility", "collapse");
            }
            if (!$navTabs.attr("hidden")) {
                $navTabs.attr("hidden", "");
            }
        } else if (currentScrollY > navHeight / 4) {
            // navHeight/4 < Y <= navHeight/2 -> show/hide based on direction
            if ($navContents.css("visibility") === "collapse") {
                $navContents.css("visibility", "");
            }
            if (currentScrollY > lastScrollY) {
                // Scroll down to hide
                if (!$navTabs.attr("hidden")) {
                    $navTabs.attr("hidden", "");
                }
            } else if (currentScrollY < lastScrollY) {
                // Scroll up to show
                if ($navTabs.attr("hidden")) {
                    $navTabs.removeAttr("hidden");
                }
            }
        } else {
            // Y <= navHeight/4 -> force show
            if ($navContents.css("visibility") === "collapse") {
                $navContents.css("visibility", "");
            }
            if ($navTabs.attr("hidden")) {
                $navTabs.removeAttr("hidden");
            }
        }

        if (currentScrollY > navHeight) {
            // Y > navHeight -> half height, tabs hidden
            if ($navBackground.css("height") !== navHeight + "px") {
                $navBackground.css("height", navHeight + "px");
            }
        } else {
            // Y <= navHeight -> hiding animation
            var bgHeight =
                navHeight + $navTabs.offset().top - $navHeader.offset().top;
            if ($navBackground.css("height") !== bgHeight + "px") {
                $navBackground.css("height", bgHeight + "px");
            }
        }

        lastScrollY = currentScrollY;
    }
    window.tabsEffectHandler = tabsEffectHandler;
    if (isDuplicate) return;

    function handleScroll() {
        window.tabsEffectHandler();
    }

    window.addEventListener("scroll", handleScroll); // handle bars hide and show
    window.addEventListener("resize", handleScroll); // handle background height

    handleScroll();

    // Block the original scroll event
    const observer = new MutationObserver((mutations) => {
        mutations.forEach((mutation) => {
            if (
                mutation.type === "attributes" &&
                mutation.attributeName === "hidden"
            ) {
                handleScroll();
            }
        });
    });

    observer.observe($navTabs[0], {
        attributes: true,
        attributeFilter: ["hidden"],
    });
});

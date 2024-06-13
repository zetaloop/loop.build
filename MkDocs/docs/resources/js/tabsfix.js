document$.subscribe(() => {
    const navTabs = document.querySelector(".md-tabs");
    const navContents = document.querySelector(".md-tabs__list");
    let lastScrollY = window.scrollY;

    function handleScroll() {
        const currentScrollY = window.scrollY;
        const navHeight = navTabs.offsetHeight;

        if (currentScrollY > navHeight / 2) {
            // Y > navHeight /2 -> force hide
            if (navContents.style.visibility === "")
                navContents.style.visibility = "collapse";
        } else if (currentScrollY > navHeight / 4) {
            // navHeight/4 < Y <= navHeight/2 -> show/hide based on scroll direction
            if (navContents.style.visibility === "collapse")
                navContents.style.visibility = "";
            if (currentScrollY > lastScrollY) {
                // Scroll down to hide
                if (!navTabs.hasAttribute("hidden"))
                    navTabs.setAttribute("hidden", "");
            } else if (currentScrollY < lastScrollY) {
                // Scroll up to show
                if (navTabs.hasAttribute("hidden"))
                    navTabs.removeAttribute("hidden");
            }
        } else {
            // Y <= navHeight / 4 -> force show
            if (navContents.style.visibility === "collapse")
                navContents.style.visibility = "";
            if (navTabs.hasAttribute("hidden"))
                navTabs.removeAttribute("hidden");
        }

        lastScrollY = currentScrollY;
    }

    window.addEventListener("scroll", handleScroll);

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

    observer.observe(navTabs, {
        attributes: true,
        attributeFilter: ["hidden"],
    });
});
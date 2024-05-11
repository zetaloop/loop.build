// Hook theme change event, fix the mess.

document$.subscribe(function () {
    var lastScheme = document.body.getAttribute("data-md-color-scheme");

    var observer = new MutationObserver(function (mutations) {
        mutations.forEach(function (mutation) {
            if (mutation.attributeName === "data-md-color-scheme") {
                newScheme = document.body.getAttribute("data-md-color-scheme");
                if (lastScheme == newScheme) return;

                // console.log("Detected data-md-color-scheme change:", newScheme);
                var elements = Array.from(
                    eval(
                        'document.querySelectorAll(".highlighttable, code, .md-typeset__table, .mermaid")'
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
                        el.classList.remove("fix-theme-fade-in");
                        void el.offsetWidth;
                        el.classList.add("fix-theme-fade-in");
                        // console.log("Fixed theme for element:", el);
                    } catch (e) {}
                });

                var tabs = document.querySelectorAll(".md-tabs")[0];
                if (tabs) {
                    tabs.classList.remove("fix-tabs-fade-in");
                    void tabs.offsetWidth;
                    tabs.classList.add("fix-tabs-fade-in");
                }

                lastScheme = newScheme;
            }
        });
    });

    observer.observe(document.body, {
        attributes: true,
        attributeFilter: ["data-md-color-scheme"],
    });
});

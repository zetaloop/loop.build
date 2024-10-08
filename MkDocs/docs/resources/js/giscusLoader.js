function loadGiscus(theme) {
  $giscus = $("#giscus-container");
  height = $giscus.height();
  $("#giscus-container").html("");
  $giscus.css("min-height", height);

  var giscusScript = document.createElement("script");
  giscusScript.src = "https://giscus.app/client.js";
  giscusScript.setAttribute("data-repo", "zetaloop/loop.comments");
  giscusScript.setAttribute("data-repo-id", "R_kgDOLrMUIA");
  giscusScript.setAttribute("data-category", "Announcements");
  giscusScript.setAttribute("data-category-id", "DIC_kwDOLrMUIM4CeiL9");
  giscusScript.setAttribute("data-mapping", "pathname");
  giscusScript.setAttribute("data-strict", "0");
  giscusScript.setAttribute("data-reactions-enabled", "1");
  giscusScript.setAttribute("data-emit-metadata", "0");
  giscusScript.setAttribute("data-input-position", "top");
  giscusScript.setAttribute("data-theme", theme);
  giscusScript.setAttribute("data-lang", "zh-CN");
  giscusScript.crossOrigin = "anonymous";
  giscusScript.async = true;

  document.getElementById("giscus-container").appendChild(giscusScript);
}

var lastTheme;
function handleRefreshGiscus() {
  if (!document.getElementById("giscus-container")) {
    return;
  }

  var palette = __md_get("__palette");
  var initialTheme =
    palette && palette.color.scheme === "slate" ? "transparent_dark" : "light";
  lastTheme = initialTheme;
  loadGiscus(initialTheme);

  var ref = document.querySelector("[data-md-component=palette]");
  ref.addEventListener("change", function () {
    var palette = __md_get("__palette");
    var newTheme =
      palette && palette.color.scheme === "slate"
        ? "transparent_dark"
        : "light";
    if (lastTheme !== newTheme) {
      lastTheme = newTheme;
      loadGiscus(newTheme);
    }
  });
}

window.addEventListener("load", () => {
  document$.subscribe(handleRefreshGiscus);
});

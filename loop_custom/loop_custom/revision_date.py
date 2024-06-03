from mkdocs_git_revision_date_localized_plugin import util
from datetime import datetime
import babel.dates


def date(date_string):
    date_obj = datetime.fromisoformat(date_string)
    return babel.dates.format_datetime(date_obj, "__LOOP__ACCURATETIME")


class Wrapper(util.Util):
    @staticmethod
    def add_spans(date_formats: util.Dict[str, str]) -> util.Dict[str, str]:
        for date_type, date_string in date_formats.items():
            if date_type == "iso_datetime":
                date_formats[date_type] = (
                    f'<span class="git-revision-date-localized-plugin git-revision-date-localized-plugin-{date_type}">'
                    f'<time class="timeago" datetime="{date_string}" title="{date(date_string)}">'
                    f"{date(date_string)}</time></span>"
                )
            else:
                date_formats[date_type] = (
                    '<span class="git-revision-date-localized-plugin git-revision-date-localized-plugin-%s">%s</span>'
                    % (date_type, date_string)
                )
        return date_formats


util.Util = Wrapper

print(
    "\033[32mINFO    -  RevisionDate patched (mkdocs_git_revision_date_localized_plugin.util.Util)\033[0m"
)

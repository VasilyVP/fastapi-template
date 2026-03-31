import json

from fastapi.responses import HTMLResponse


def versioned_swagger_ui_html(doc_versions: list[dict[str, str]], title: str) -> HTMLResponse:
    """Render Swagger UI with a version-selector dropdown.

    FastAPI's built-in get_swagger_ui_html() always injects a single `url`
    property that overrides `urls` and breaks the dropdown, so the HTML is
    rendered directly instead.
    """
    versions_json = json.dumps(doc_versions)
    primary = doc_versions[0]["name"]
    html = f"""<!DOCTYPE html>
<html>
  <head>
    <title>{title}</title>
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css">
  </head>
  <body>
    <div id="swagger-ui"></div>
    <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-standalone-preset.js"></script>
    <script>
      window.onload = function () {{
        SwaggerUIBundle({{
          urls: {versions_json},
          "urls.primaryName": "{primary}",
          dom_id: "#swagger-ui",
          presets: [
            SwaggerUIBundle.presets.apis,
            SwaggerUIStandalonePreset,
          ],
          plugins: [SwaggerUIBundle.plugins.DownloadUrl],
          layout: "StandaloneLayout",
        }})
      }}
    </script>
  </body>
</html>"""
    return HTMLResponse(html)

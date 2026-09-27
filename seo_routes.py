"""SEO, crawl directives and structured-data integration."""
import json
import xml.sax.saxutils as sax
from flask import Response, request

BASE="https://easewithpy.de5.net"

def install(app, mod, all_courses, layout=None):
    def robots():
        return Response(
            "User-agent: *\n"
            "Allow: /\n"
            "Disallow: /dashboard\n"
            "Disallow: /login\n"
            "Disallow: /register\n"
            "Disallow: /logout\n"
            "Disallow: /api/\n"
            f"Sitemap: {BASE}/sitemap.xml\n",
            mimetype="text/plain",
        )

    def sitemap():
        urls=[("/", "1.0"),("/courses","0.9"),("/academy","0.8"),("/practice","0.8"),("/roadmap","0.7"),("/projects","0.7"),("/cheatsheets","0.7"),("/glossary","0.6"),("/challenges","0.7"),("/tools","0.7"),("/about","0.3"),("/terms","0.2"),("/privacy","0.2"),("/disclaimer","0.2")]
        for course in all_courses():
            urls.append((course["href"],"0.8"))
            if course["slug"]=="python":
                urls.extend((f"/learn/{x['n']}","0.6") for x in course["lessons"])
            else:
                urls.extend((f"/learn/{course['slug']}/{i}","0.6") for i in range(1,len(course["lessons"])+1))
        body="".join(f"<url><loc>{sax.escape(BASE+p)}</loc><changefreq>monthly</changefreq><priority>{pr}</priority></url>" for p,pr in urls)
        return Response('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+body+"</urlset>",mimetype="application/xml")

    def llms():
        text="""# LearnPython

> LearnPython is an educational coding platform for learning programming through lessons, practice labs, and projects.

## Main pages
- Home: https://easewithpy.de5.net/
- Courses: https://easewithpy.de5.net/courses
- About: https://easewithpy.de5.net/about
- Terms: https://easewithpy.de5.net/terms
- Privacy: https://easewithpy.de5.net/privacy
- Educational disclaimer: https://easewithpy.de5.net/disclaimer

## Course content
Python, AI Fundamentals, Go, TypeScript, HTML, CSS, JavaScript, SQL, and Git & GitHub.

## Important
Course material and code examples are provided for educational and informational purposes only. Verify important security, legal, financial, operational, and production decisions against authoritative sources.
"""
        return Response(text,mimetype="text/plain")

    app.add_url_rule("/robots.txt","seo_robots",robots)
    app.add_url_rule("/sitemap.xml","seo_sitemap",sitemap)
    app.add_url_rule("/llms.txt","seo_llms",llms)

    @app.after_request
    def seo_headers(response):
        response.headers.setdefault("X-Content-Type-Options","nosniff")
        response.headers.setdefault("Referrer-Policy","strict-origin-when-cross-origin")
        if response.content_type and "text/html" in response.content_type:
            response.headers.setdefault("X-Frame-Options","SAMEORIGIN")
            try:
                body=response.get_data(as_text=True)
                if "<head>" in body:
                    body=body.replace("<head>","<head><meta name=\"referrer\" content=\"strict-origin-when-cross-origin\">",1)
                path=request.path
                if path.startswith("/courses/") and path.count("/") == 2:
                    slug=path.rsplit("/",1)[-1]
                    course=next((x for x in all_courses() if x["slug"]==slug),None)
                    if course and "BreadcrumbList" not in body:
                        data={"@context":"https://schema.org","@type":"Course","name":course["title"],"description":course["description"],"provider":{"@type":"Organization","name":"LearnPython","url":BASE},"url":BASE+path,"isAccessibleForFree":True}
                        bread={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
                            {"@type":"ListItem","position":1,"name":"Home","item":BASE+"/"},
                            {"@type":"ListItem","position":2,"name":"Courses","item":BASE+"/courses"},
                            {"@type":"ListItem","position":3,"name":course["title"],"item":BASE+path}
                        ]}
                        script='<script type="application/ld+json">'+json.dumps(data,separators=(",",":"))+"</script>"
                        script+='<script type="application/ld+json">'+json.dumps(bread,separators=(",",":"))+"</script>"
                        body=body.replace("</head>",script+"</head>",1)
                response.set_data(body)
            except Exception:
                pass
        return response

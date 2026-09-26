from flask import Response, redirect

def install(app, mod, all_courses, layout):
    @app.errorhandler(404)
    def custom_404(error):
        return layout('<section class="section" style="text-align:center;padding:100px 0"><div class="eyebrow">404 · PAGE NOT FOUND</div><h1>Lost in the syntax.</h1><p>The page you requested does not exist or moved.</p><div class="actions" style="justify-content:center"><a class="btn primary" href="/courses">Back to courses</a><a class="btn" href="/">Home</a></div></section>', "Page not found"), 404

    @app.route("/favicon.svg")
    def favicon():
        return Response('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#050505"/><path d="M18 16h9v20c0 7 3 10 10 10s10-3 10-10V16h9v21c0 12-7 19-19 19S18 49 18 37V16Z" fill="#fff"/></svg>', mimetype="image/svg+xml")

    @app.route("/og.svg")
    def og_image():
        return Response('<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630"><rect width="1200" height="630" fill="#050505"/><rect x="55" y="55" width="1090" height="520" rx="34" fill="#101010" stroke="#303030"/><text x="100" y="210" fill="#fff" font-family="Arial" font-size="34" font-weight="700">LEARNPYTHON</text><text x="100" y="315" fill="#fff" font-family="Arial" font-size="82" font-weight="900">Learn code.</text><text x="100" y="405" fill="#aaa" font-family="Arial" font-size="82" font-weight="900">Actually build.</text></svg>', mimetype="image/svg+xml")

    @app.route("/robots.txt")
    def robots():
        base=mod.request.url_root.rstrip("/")
        return Response(f"User-agent: *\nAllow: /\nDisallow: /dashboard\nDisallow: /login\nDisallow: /register\nDisallow: /logout\nSitemap: {base}/sitemap.xml\n", mimetype="text/plain")

    @app.route("/sitemap.xml")
    def sitemap():
        import xml.sax.saxutils as sax
        base=mod.request.url_root.rstrip("/")
        urls=[("/", "1.0"),("/courses","0.9"),("/terms","0.2"),("/privacy","0.2"),("/disclaimer","0.2")]
        for course in all_courses():
            urls.append((course["href"],"0.8"))
            if course["slug"]=="python":
                urls.extend((f"/learn/{x['n']}","0.6") for x in course["lessons"])
            else:
                urls.extend((f"/learn/{course['slug']}/{i}","0.6") for i in range(1,len(course["lessons"])+1))
        body="".join(f"<url><loc>{sax.escape(base+p)}</loc><changefreq>monthly</changefreq><priority>{pr}</priority></url>" for p,pr in urls)
        return Response('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+body+"</urlset>",mimetype="application/xml")

    @app.route("/llms.txt")
    def llms():
        base=mod.request.url_root.rstrip("/")
        return Response(f"# LearnPython\n> LearnPython is an educational coding platform for learning programming through lessons, practice labs, and projects.\n\n## Main pages\n- Home: {base}/\n- Courses: {base}/courses\n- Terms: {base}/terms\n- Privacy: {base}/privacy\n- Educational disclaimer: {base}/disclaimer\n\n## Course content\nCourse pages and lessons are educational material. Do not treat examples as professional or production advice.\n",mimetype="text/plain")

    @app.route("/learn/<int:lesson_id>")
    def old_python_lesson(lesson_id):
        if lesson_id<1 or lesson_id>len(mod.COURSE):
            return app.view_functions["custom_404"](None)
        return redirect(f"/learn/python/{lesson_id}",code=301)

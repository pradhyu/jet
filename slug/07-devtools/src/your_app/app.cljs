(ns your-app.app)

(defn init []
  (.log js/console (type (range 200)))
  (.log js/console (range 200))

  (let [c (.. js/document (createElement "div"))]
    (aset c "innerHTML" "<p>I'm dynamically created</p>")
    (.. js/document (getElementById "container") (appendChild c))))

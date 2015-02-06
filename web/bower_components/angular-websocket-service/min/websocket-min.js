"use strict";var websocketModule=angular.module("websocket",[]).factory("$websocket",["$rootScope",function(e){var n=function(e,n){return e+" "+JSON.stringify(n)+"\n"},o=function(e){var n,o,t;return t=e.split(" ",1),n=t[0],o=JSON.parse(e.substring(n.length+1)),{topic:n,body:o}},t=function(e,n){e.ready?e.websocket.send(n):e.queue.push(n)},c=function(e){console.log("opened socket",e.endpoint),e.ready=!0,e.queue.length&&e.queue.forEach(function(n){t(e,n)}),e.queue=[]},r=function(e,n){console.log("socket error",e.endpoint,n)},i=function(n,t){var c;c=o(t.data),"/refresh"==c.topic&&window.location.reload(),u(n,c.topic,c.body),e.$apply()},s=function(e,n,o,t){t||(t={}),"exact"in t||(t.exact=!1),e.listeners[n]||(e.listeners[n]=[]),-1==e.listeners[n].indexOf(o)&&e.listeners[n].push({callback:o,options:t})},u=function(e,n,o){var t=[];Object.keys(e.listeners).forEach(function(c){0===n.indexOf(c)&&e.listeners[c].forEach(function(e){e.options.exact&&c!=n||-1==t.indexOf(e.callback)&&(e.callback(n,o),t.push(e.callback))})})};return{connect:function(e){var o={endpoint:e,websocket:null,ready:!1,queue:[],listeners:{},emit:function(e,o){t(this,n(e,o))},register:function(e,n,o){s(this,e,n,o)}};return console.log("connect to",e),o.websocket=new window.WebSocket(e),o.websocket.onopen=function(){return c(o)},o.websocket.onerror=function(e){return r(o,e)},o.websocket.onmessage=function(e){return i(o,e)},o}}}]);
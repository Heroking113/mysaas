(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([[2],{189:function(t,n,r){"use strict";r.r(n);var e=r(201);var o=r(195);for(var u in o)if(u!=="default")(function(t){r.d(n,t,(function(){return o[t]}))})(u);var a=r(10);var i=Object(a["a"])(o["default"],e["a"],e["b"],false,null,"a17d97cc",null);n["default"]=i.exports},195:function(t,n,r){"use strict";r.r(n);var e=r(196);var o=r.n(e);for(var u in e)if(u!=="default")(function(t){r.d(n,t,(function(){return e[t]}))})(u);n["default"]=o.a},196:function(t,n,r){"use strict";Object.defineProperty(n,"__esModule",{value:true});n.default=void 0;var e={components:{},data:function t(){return{scriptCommand:""}},beforeMount:function t(){},methods:{toTaskRecord:function t(){this.$router.push({path:"/taskrecord"})},getScriptCommand:function t(){var n=this;this.$http.post(window.API_ROOT+"/execute_mission/").then((function(t){n.scriptCommand=t.data}))}}};n.default=e},201:function(t,n,r){"use strict";var e=function(){var t=this;var n=t.$createElement;var r=t._self._c||n;return r("div",[r("h1",[t._v("执行任务界面")]),t._v(" "),r("button",{on:{click:t.toTaskRecord}},[t._v("任务记录")])])};var o=[];r.d(n,"a",(function(){return e}));r.d(n,"b",(function(){return o}))}}]);
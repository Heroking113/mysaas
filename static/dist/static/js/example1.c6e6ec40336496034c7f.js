(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([[2],{305:function(t,e,a){"use strict";a.r(e);var i=a(321);var s=a(309);for(var n in s)if(n!=="default")(function(t){a.d(e,t,function(){return s[t]})})(n);var l=a(318);var r=a(12);var o=Object(r["a"])(s["default"],i["a"],i["b"],false,null,"66fe6e0e",null);e["default"]=o.exports},309:function(t,e,a){"use strict";a.r(e);var i=a(310);var s=a.n(i);for(var n in i)if(n!=="default")(function(t){a.d(e,t,function(){return i[t]})})(n);e["default"]=s.a},310:function(t,e,a){"use strict";var i=a(3);Object.defineProperty(e,"__esModule",{value:true});e.default=void 0;var s=i(a(98));var n=i(a(99));var l={components:{},data:function t(){return{HostData:[],BusinessData:[],bk_biz_id:"",MissionData:[],content:"",selected_bk_biz_id:"",selected_script_content:"",selected_hosts:[]}},created:function t(){var e=this;this.$http.get("/query_all_info/").then(function(t){if(t.data.result){var a=t.data.data;if(a.host_data){e.HostData=a.host_data}if(a.business_data){e.BusinessData=a.business_data}e.MissionData=a.mission_data;e.BusinessData.unshift({bk_biz_id:0,bk_biz_name:"所有任务"})}else{e.$message.error("获取信息失败！")}})},mounted:function t(){(0,s.default)("#execute").click(function(){(0,s.default)("#execute").css("background","#008272")})},methods:{onSubmit:function t(){var e=this;if(!(0,s.default)("#cur_business").val()){this.$message.warning("请选择业务");return}if(!(0,s.default)("#cur_mission").val()){this.$message.warning("请选择任务");return}if(this.selected_hosts.length===0){this.$message.warning("请选择主机");return}var a=document.cookie.split(";");var i="";for(var n in a){if(a[n].indexOf("csrftoken")!=-1){var i=a[n].split("=")[1]}}var l={bk_biz_id:this.selected_bk_biz_id,business_name:(0,s.default)("#cur_business").val(),mission_name:(0,s.default)("#cur_mission").val(),host_list:JSON.stringify(this.selected_hosts)};this.$http.post("/execute_script/",l,{headers:{"X-CSRFToken":i}}).then(function(t){e.$message.warning("任务正在执行, 请勿重复提交")})},goRecord:function t(){this.$router.push({path:window.PROJECT_CONFIG.SITE_URL+"task-record"})},get_select_business_label:function t(e){var a=this;this.selected_bk_biz_id=e;var i="/query_host_by_business/?bk_biz_id="+this.selected_bk_biz_id;this.$http.get(i).then(function(t){if(t.data.result){a.HostData=t.data.data}else{a.$message.error("获取当前业务下的主机信息失败！")}})},get_select_script_content:function t(e){this.selected_script_content=e},handleSelectionChange:function t(e){this.selected_hosts=e}}};e.default=l},311:function(t,e,a){},318:function(t,e,a){"use strict";var i=a(311);var s=a.n(i);var n=s.a},321:function(t,e,a){"use strict";var i=function(){var t=this;var e=t.$createElement;var a=t._self._c||e;return a("div",[a("el-container",[a("el-header",{staticClass:"head-left-content"},[a("el-button",{staticClass:"navibar-button-style",staticStyle:{"background-color":"#0a6659"},attrs:{id:"execute",type:"primary"}},[t._v("执行任务")]),t._v(" "),a("el-button",{staticClass:"navibar-button-style",attrs:{type:"primary"},on:{click:t.goRecord}},[t._v("任务记录")])],1)],1),t._v(" "),a("div",{staticClass:"table-style"},[a("el-form",{staticClass:"demo-form-inline",attrs:{inline:true}},[a("el-form-item",{attrs:{label:"选择业务"}},[a("el-select",{ref:"select_business",staticStyle:{width:"160px"},attrs:{id:"cur_business",placeholder:"请选择"},on:{change:t.get_select_business_label},model:{value:t.bk_biz_id,callback:function(e){t.bk_biz_id=e},expression:"bk_biz_id"}},t._l(t.BusinessData,function(t){return a("el-option",{key:t.bk_biz_id,attrs:{label:t.bk_biz_name,value:t.bk_biz_id}})}),1)],1),t._v(" "),a("el-form-item",{attrs:{label:"选择任务"}},[a("el-select",{ref:"select_script",staticStyle:{width:"280px"},attrs:{id:"cur_mission",placeholder:"请选择"},on:{change:t.get_select_script_content},model:{value:t.content,callback:function(e){t.content=e},expression:"content"}},t._l(t.MissionData,function(t){return a("el-option",{key:t.mission_content,attrs:{label:t.mission_name,value:t.mission_content}})}),1)],1),t._v(" "),a("el-form-item",[a("el-button",{attrs:{type:"primary"},on:{click:t.onSubmit}},[t._v("执行")])],1)],1),t._v(" "),a("hr",{staticStyle:{FILTER:"alpha(opacity=100,finishopacity=0,style=3)"},attrs:{width:"100%",color:"gray",size:"1"}}),t._v(" "),a("el-table",{ref:"multipleTable",staticStyle:{width:"100%"},attrs:{border:"",data:t.HostData,"tooltip-effect":"dark"},on:{"selection-change":t.handleSelectionChange}},[a("el-table-column",{attrs:{align:"center",type:"selection",width:"55"}}),t._v(" "),a("el-table-column",{attrs:{align:"center",prop:"bk_cloud_id",label:"云区域ID",width:"100"}}),t._v(" "),a("el-table-column",{attrs:{align:"center",prop:"bk_cpu",label:"核数",width:"100"}}),t._v(" "),a("el-table-column",{attrs:{align:"center",prop:"bk_os_name",label:"操作系统",width:"150"}}),t._v(" "),a("el-table-column",{attrs:{align:"center",prop:"bk_host_innerip",label:"内网IP",width:"150"}}),t._v(" "),a("el-table-column",{attrs:{align:"center",prop:"bk_host_id",label:"主机ID",width:"150"}}),t._v(" "),a("el-table-column",{attrs:{align:"center",prop:"bk_os_bit",label:"位数",width:"150"}}),t._v(" "),a("el-table-column",{attrs:{align:"center",prop:"create_time",label:"创建时间",width:"300"}})],1)],1)],1)};var s=[];a.d(e,"a",function(){return i});a.d(e,"b",function(){return s})}}]);
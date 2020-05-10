<template>
    <div class="king-page-box">
        <div class="king-layout1-header">
            <nav>
                <div style="overflow:hidden; z-index: inherit;" class="navbar king-horizontal-nav1  f14">
                    <div class="navbar-container">
                        <ul class="nav navbar-nav pull-left m0">
                            <li class="active"><a href="javascript:void(0);">执行任务</a></li>
                            <li><a href="javascript:void(0);" onclick="javascript:location.href='/taskrecord'">任务记录</a></li>
                        </ul>
                    </div>
                </div>
            </nav>
        </div>
        <div class="king-layout2-main mt15" style="width:960px;">
            <form class="form-vertical p15">
                <div class="form-group ">
                    <label>选择业务：</label>
                    <select class="form-control">
                        <option value="选择项1">选择项1</option>
                        <option value="选择项2">选择项2</option>
                        <option value="选择项3">选择项3</option>
                        <option value="选择项4">选择项4</option>
                    </select>
                </div>
            </form>
            <form class="form-vertical p15">
                <div class="form-group ">
                    <label>选择脚本：</label>
                    <select class="form-control">
                        <option value="选择项1">选择项1</option>
                        <option value="选择项2">选择项2</option>
                        <option value="选择项3">选择项3</option>
                        <option value="选择项4">选择项4</option>
                    </select>
                </div>
            </form>
            <form class="form-horizontal">
                <div class="form-group clearfix">
                    <div class="col-sm-9 col-sm-offset-3">
                        <button type="button" class="king-btn mr10  king-success">执行</button>
                    </div>
                </div>
                <table class="table mb0 pr15 ranger-box2">
                    <thead>
                        <tr>
                            <th><input type="checkbox"></th>
                            <th style="width: 70px;">序号</th>
                            <th style="width: 15%;">IP</th>
                            <th style="width: 15%;">操作系统</th>
                            <th>操作</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <th><input type="radio"></th>
                            <td style="width: 70px;">1</td>
                            <td style="width: 15%;">127.0.0.1</td>
                            <td style="width: 15%;">Windows10</td>
                            <td>
                                <button class="btn btn-xs btn-success"> <i class="glyphicon glyphicon-ok"></i> </button>
                                <button class="btn btn-xs btn-warning"> <i class="glyphicon glyphicon-edit"></i> </button>
                                <button class="btn btn-xs btn-danger"> <i class="glyphicon glyphicon-remove"></i> </button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </form>
        </div>
    </div>
</template>

<script>
    import $ from 'jquery'
    export default {
        components: {
        },
        beforeMount () {
            this.$http.get('execute_task/').then(resp => {
                console.log(resp)
            })
            console.log('befeoreMount')
        },
        mounted () {
            $('button').click(function (e) {
                alert('little bro.')
            })
        },
        methods: {
            
        }
    }
</script>

<style scoped>
</style>

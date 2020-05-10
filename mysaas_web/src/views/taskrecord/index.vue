<template>
    <div class="king-page-box">
        <div class="king-layout1-header">
            <nav class="">
                <div style="overflow:hidden; z-index: inherit;" class="navbar king-horizontal-nav1  f14">
                    <div class="navbar-container">
                        <ul class="nav navbar-nav pull-left m0">
                            <li><a href="javascript:void(0);" onclick="javascript:location.href='/executetask'">执行任务</a></li>
                            <li class="active"><a href="javascript:void(0);">任务记录</a></li>
                        </ul>
                    </div>
                </div>
            </nav>
        </div>
        <div class="king-layout2-main mt15" style="width:960px;">
            <form class="form-vertical p15">
                <div class="form-group ">
                    <label>业务</label>
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
                    <label>用户</label>
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
                    <label>任务</label>
                    <select class="form-control">
                        <option value="选择项1">选择项1</option>
                        <option value="选择项2">选择项2</option>
                        <option value="选择项3">选择项3</option>
                        <option value="选择项4">选择项4</option>
                    </select>
                </div>
            </form>
            <div class="form-group clearfix">
                <div class="col-sm-9 col-sm-offset-3">
                    <button type="button" class="king-btn mr10  king-success">提交</button>
                </div>
            </div>
            <form action="" class="form-horizontal">
                <fieldset>
                    <div class="control-group">
                        <div class="controls date form_datetime" data-date="1979-09-16T05:25:07Z" data-date-format="dd MM yyyy - HH:ii p" data-link-field="dtp_input1">
                            <span class="add-on"><i class="icon-th"></i>选择</span>
                            <input size="25" type="text" value="" readonly>
                            <span class="add-on"><i class="icon-remove"></i>清除</span>
                        </div>
                    </div>
                </fieldset>
            </form>
            <form class="form-horizontal">
                <table class="table mb0 pr15 ranger-box2  ">
                    <thead>
                        <tr>
                            <!--<th><input type="checkbox"/></th>-->
                            <th style="width: 12.5%;">业务</th>
                            <th style="width: 12.5%;">用户</th>
                            <th style="width: 12.5%;">任务</th>
                            <th style="width: 12.5%;">操作时间</th>
                            <th style="width: 12.5%;">机器数</th>
                            <th style="width: 12.5%;">状态</th>
                            <th style="width: 12.5%;">参数</th>
                            <th style="width: 12.5%;">详情</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td style="width: 12.5%;">业务</td>
                            <td style="width: 12.5%;">用户</td>
                            <td style="width: 12.5%;">任务</td>
                            <td style="width: 12.5%;">操作时间</td>
                            <td style="width: 12.5%;">机器数</td>
                            <td style="width: 12.5%;">状态</td>
                            <td style="width: 12.5%;">参数</td>
                            <td style="width: 12.5%;">详情</td>
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
        data () {
            return {
            }
        },
        mounted () {
            $('button').click(function (e) {
                console.log(e)
            })
        },
        methods: {
        }
    }
</script>

<style scoped>
</style>

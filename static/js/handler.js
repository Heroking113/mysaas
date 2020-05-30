$(document).ready(function () {
    var getUserHostInfoUrl = window.location.protocol+ "//" + window.location.host + "/get-host-info/";
    $("#choose_business").change(function () {
        var param = {
            'business_name': $("#choose_business").val()
        };
        $.ajax({
                cache: false,
                type: 'GET',
                data: param,
                dataType: 'json',
                url: getUserHostInfoUrl,
                // 下面的headers和contentType是请求Django后台所必须的配置
                contentType: 'application/x-www-form-urlencoded',
                success: function (resp) {
                    var html = '';
                    var host_data = resp.host_data;
                    for(let i=0;i<host_data.length;i++){
                        html +=
                            `
                            <tr id="host_info_list">
                                <td style="width: 40%;">${host_data[i].host.bk_host_innerip}</td>
                                <td style="width: 40%;">${host_data[i].host.bk_os_name}</td>
                                <td style="width: 20%">
                                    <a href="javascript:void(0);" class="bk-text-button">待定</a>
                                </td>
                            </tr>
                            `;
                    }
                    $("#host_info_list").html(html);
                }
            });
    });
});
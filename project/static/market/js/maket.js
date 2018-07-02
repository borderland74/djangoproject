$(document).ready(function () {
    var url = location.href;

    spanIdStr = "yellow" +  url.split("/")[4];
    $yellowSpan = $(document.getElementById(spanIdStr));
    $yellowSpan.addClass("yellowSlide")
        $("#allTypeBtn").bind("click", function () {
        $("#typediv").toggle();
        $("#sortdiv").hide();
    });
    $("#allSortBtn").bind("click", function () {
        $("#sortdiv").toggle();
        $("#typediv").hide();
    });
    $("#typediv").bind("click", func);
    $("#sortdiv").bind("click", func);
    function func() {
        $(this).hide()
    }

     //给分类添加颜色
    aIdStr = "type" + url.split("/")[5];
    $a = $(document.getElementById(aIdStr));
    $a.addClass("abg");

    // function changeCart (data) {
    //     var flag = $(this).attr("flag");
    //     var gid = $(this).attr("gid");
    //     var cid = $(this).attr("cid");
    //     var pid = $(this).attr("pid");
    //     $.ajax({
    //         url:"/changcart"+flag+"/",
    //         data:{"gid":gid,"cid":cid,"pid":pid},
    //         dataType:"json",
    //         type:"post",
    //         success:function (data,status) {
    //             console.log(data)
    //
    //         }
    //     })
    //
    //
    // }
    // $("#subBtn").bind("click",changeCart);
    // $("#addBtn").bind("click",changeCart);
        function changeCart(){
        var flag = $(this).attr("flag");
        //组id  子组id  商品id
        var gid = $(this).attr("gid");
        var cid = $(this).attr("cid");
        var pid = $(this).attr("pid");
        console.log(gid,cid,pid);
        //发起ajax请求，添加购物车
        $.post("/changecart/"+flag+"/", {"gid":gid,"cid":cid,"pid":pid}, function (data, status) {
            if (data.error){
                location.href = "http://127.0.0.1:8000/login/"
            } else {
                $(document.getElementById(pid)).html(data.num)
            }
        });
    }


    //添加购物车
    $(".addBtn").bind("click", changeCart);
    $(".subBtn").bind("click", changeCart);

});
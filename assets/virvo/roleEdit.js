(function($,window){
    var roleId = $("#idStr").val();
    var roleEdit = {
        //初始化
        init: function(){
            //操作权限 
            var setpermissionEdit = {
                async : {
                    url : "role/choicePermissionTree/",
                    type : "post",
                    enable : true,
                    autoParam : [ "id" ],
                    dataType : "json",
                    otherParam : {
                        "roleId" : roleId
                    }
                },
                check : {
                    enable : true,
                    chkStyle : "checkbox",
                    chkboxType : {
                        "Y" : "ps",
                        "N" : "ps"
                    }, 
                    radioType : "all"
                },
                view : {
                    dblClickExpand : false
                },
                data : {
                    simpleData : {
                        enable : true
                    }
                },
                callback : {
                    beforeClick : roleEdit.beforeClickPermissionEdit,
                    beforeCheck: roleEdit.zTreeBeforeCheck,
                    onCheck : roleEdit.onCheckPermissionEdit
                }
            }
            $.fn.zTree.init($("#permissionEditDemo"), setpermissionEdit, null);
            $.fn.zTree.getZTreeObj("permissionEditDemo").expandAll(true);
            $(".modal-body").addClass("modal-body-overflow");
        },
        beforeClickPermissionEdit: function(treeId, treeNode){
            var zTree = $.fn.zTree.getZTreeObj("permissionEditDemo");
            zTree.checkNode(treeNode, !treeNode.checked, true, true);
            return false;
        },
        zTreeBeforeCheck: function(treeId, treeNode){
            var flag;
            var zTree = $.fn.zTree.getZTreeObj("permissionEditDemo");
            if(treeNode.isParent){
                flag = true;
            }else{
                flag = false;
                zTree.checkNode(treeNode, !treeNode.checked, !treeNode.checked);
            };
            return flag;
        },
        onCheckPermissionEdit: function(e, treeId, treeNode){
            var zTree = $.fn.zTree.getZTreeObj("permissionEditDemo"), nodes = zTree
                .getCheckedNodes(true), v = "";
            for (var i = 0, l = nodes.length; i < l; i++) {
                v += nodes[i].name + ",";
            }
        },
        doSubmit: function(){
            var list = [];
            var editlist = [];
            var checkNodes = $.fn.zTree.getZTreeObj("permissionEditDemo").getNodesByParam("checked", true);
            if (checkNodes != null && checkNodes.length > 0) {
                for (var i = 0; i < checkNodes.length; i++) {
                    var obj = {};
                    if (checkNodes[i].type == "premissionEdit") { // 可写 
                        editlist.push(checkNodes[i].pId); 
                        console.log(checkNodes[i].id,checkNodes[i].name);
                    }
                    else{
                        obj.id = checkNodes[i].id;
                        obj.edit = false;
                        list.push(obj);
                        console.log(checkNodes[i].id,checkNodes[i].name);
                    }
                    
                }
            }
            console.log('editlist:',editlist);
            console.log('list:',list);
            //重组可写的权限 
            if (list.length > 0 && editlist.length >0) {
                for (var i = 0; i < list.length; i++) {
                    for (var j =0; j< editlist.length; j++) {
                        if (list[i].id == editlist[j]) {
                            list[i].edit = true;
                            // console.log(checkNodes[i].name);
                        }
                    }
                }
            }
            console.log('list after:',list);
            $("#permissionTree").val(JSON.stringify(list));
            console.log(JSON.stringify(list));
            $("#role_update_form").ajaxSubmit(function(data) {
                    if (data != null) {
                        //var result = $.parseJSON(data);
                        $("#commonSmWin").modal("hide");
                        
                        // if (result.success) {
                        //     if (result.obj.flag == 1){
                        //         $("#commonSmWin").modal("hide");
                        //         layer.msg("修改成功！",{move:false});
                        //         myTable.refresh()
                        //     }else{
                        //         layer.msg(result.obj.errMsg,{move:false});
                        //     }
                        // }else{
                        //     layer.msg(result.msg,{move:false});
                        // }
                    }
                });
            
            // if(roleEdit.validates()){
            //     $("#editForm").ajaxSubmit(function(data) {
            //         if (data != null) {
            //             var result = $.parseJSON(data);
            //             if (result.success) {
            //                 if (result.obj.flag == 1){
            //                     $("#commonSmWin").modal("hide");
            //                     layer.msg("修改成功！",{move:false});
            //                     myTable.refresh()
            //                 }else{
            //                     layer.msg(result.obj.errMsg,{move:false});
            //                 }
            //             }else{
            //                 layer.msg(result.msg,{move:false});
            //             }
            //         }
            //     });
            // }
        },
        //校验
        validates: function(){
            return $("#editForm").validate({
                rules : {
                    roleName : {
                        required : true,
                        maxlength : 20,
                        minlength : 1
                    },
                    description : {
                        maxlength : 140
                    }
                },
                messages : {
                    roleName : {
                        required : roleNameNull,
                        maxlength : publicSize20,
                        minlength : publicMinSize1Length
                    },
                    description : {
                        maxlength : publicSize140
                    }
                }
            }).form();
        },
    }
    $(function(){
        roleEdit.init();
        // $('input').inputClear();

        // //优先级策略单选组选择
        // $(".priority-group").on("click","input",function () {
        //     $(".priority-group input").prop("checked",false);
        //     $(this).prop("checked",true)
        // });

        $("#doSubmitEdit").on("click",roleEdit.doSubmit);
    })
})($,window)
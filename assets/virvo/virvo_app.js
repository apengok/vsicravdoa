function load_Tree(page_name)
{
   var _this = this;
   // zTree 的参数配置，深入使用请参考 API 文档（setting 配置详解）
   var setting = {
      view: {
        fontCss: getFont,
        nameIsHTML: true,
      },
      callback: {
        onNodeCreated: zTreeOnNodeCreated
      },
      // callback:{
      //   onClick:function(){_this.slotSelectChanged();}
      // },
      data: {
        simpleData: {
          enable: true
        }
      }
    };

    function zTreeOnNodeCreated(event, treeId, treeNode) {
        // alert(treeNode.tId + ", " + treeNode.name);
        var aObj = $("#" + treeNode.tId + "_a");
        aObj.addClass("J_menuItem");
        // alert(aObj.class);
    };

    function getFont(treeId, node) {
      return node.font ? node.font : {};
    }

        
    $.ajax({
        type:"GET",
        url:"/dma/gettree/" , 
        dataType: "json",
        // data:{'csrfmiddlewaretoken': '{{ csrf_token }}'},
        data:{'page_name': page_name},
        success:function(res){
            var json = res['trees']   
            // console.log(json);    
            $.fn.zTree.init($("#station_tree"), setting, json);
            var zTree = $.fn.zTree.getZTreeObj("station_tree");
            
        }
    });
}        


function load_dmaTree()
    {
       var _this = this;
       // zTree 的参数配置，深入使用请参考 API 文档（setting 配置详解）
       var setting = {
          view: {
            fontCss: getFont,
            nameIsHTML: true,
            addDiyDom: addDiyDom
          },
          // callback:{
          //   onClick:function(){_this.slotSelectChanged();}
          // },
          data: {
            simpleData: {
              enable: true
            }
          }
        };

        function getFont(treeId, node) {
          return node.font ? node.font : {};
        }

        var IDMark_A = "_a";

        function addDiyDom(treeId, treeNode) {
          if (treeNode.parentNode && treeNode.tid!=1) return;

          if (treeNode.name != '威尔沃') return;
          var aObj = $("#" + treeNode.tId + IDMark_A);

          
          var editStr = '<img id="diyBtn_add" class="img " src="/static/virvo/images/add.png" tabindex="0" onfocus="this.blur()"; style="outline: none;">';
          
          aObj.after(editStr);
          console.log(aObj);
          var btn = $("#diyBtn_add");
          if (btn) btn.bind("click", function(){
            $("#new-form-modal").modal();
          });
        
        }
            
        $.ajax({
            type:"GET",
            url:"/dma/getdmatree/" , 
            dataType: "json",
            // data:{'csrfmiddlewaretoken': '{{ csrf_token }}'},
            
            success:function(res){
                var json = res['trees']   
                console.log(json);    
                $.fn.zTree.init($("#dma_tree"), setting, json);
                var zTree = $.fn.zTree.getZTreeObj("dma_tree");
                
            }
        });
    }    

function slotSelectChanged()
    {
      var zTree = $.fn.zTree.getZTreeObj("treeDemo");
      
      var nodes = zTree.getSelectedNodes();
      if (nodes.length) {
        var n = nodes[0]
        console.log(n.name)

        $.ajax({
            type:"GET",
            // url:"/virvo/gettreenode/" , 
            url:"/dma/" + n.id,
            dataType: "html",
            
            
            success:function(res){
                 
                // $("#collapse1").html(res)
                
                $('#myModal').on('shown.bs.modal', function () {
                    load_station_map();
                 })
            },
            error:function(res){
              console.log("error?")
              console.log(res);
            }
        });

      }
      
    }

function load_stationTree()
    {
       var _this = this;
       // zTree 的参数配置，深入使用请参考 API 文档（setting 配置详解）
       var setting = {
          view: {
            fontCss: getFont,
            nameIsHTML: true,
            // addDiyDom: addDiyDom
          },
          // callback:{
          //   onClick:function(){_this.slotSelectChanged();}
          // },
          data: {
            simpleData: {
              enable: true
            }
          }
        };

        function getFont(treeId, node) {
          return node.font ? node.font : {};
        }

        var IDMark_A = "_a";

        function addDiyDom(treeId, treeNode) {
          if (treeNode.parentNode && treeNode.tid!=1) return;

          if (treeNode.name != '威尔沃') return;
          var aObj = $("#" + treeNode.tId + IDMark_A);

          console.log(treeId);
          console.log(treeNode.id);
          console.log(treeNode.name);
          //if (treeNode.id == 1) {
            var editStr = '<img id="diyBtn_add" class="img " src="/static/virvo/images/add.png" tabindex="0" onfocus="this.blur()"; style="outline: none;">';
            
            aObj.after(editStr);
            console.log(aObj);
            var btn = $("#diyBtn_add");
            if (btn) btn.bind("click", function(){
              $("#new-form-modal").modal();
            });
          //}
        }
            
        $.ajax({
            type:"GET",
            url:"/dma/getstationtree/" , 
            dataType: "json",
            // data:{'csrfmiddlewaretoken': '{{ csrf_token }}'},
            
            success:function(res){
                var json = res['trees']   
                // console.log(json);    
                $.fn.zTree.init($("#station_tree"), setting, json);
                var zTree = $.fn.zTree.getZTreeObj("station_tree");
                
            }
        });
    }    
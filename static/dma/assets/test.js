
/***********************底图应用层部分***********************/
var appLayer = function (options) {
   var layer = new ol.layer.Tile({
   extent: ol.proj.transformExtent(options.mapExtent, options.fromProject, options.toProject),
   source: new ol.source.XYZ({
		urls: options.urls,
		tilePixelRatio: options.tilePixelRatio,
		minZoom: options.mapMinZoom,
		maxZoom: options.mapMaxZoom
		})
   });
   return layer;
}

var latitude = 114.3524087439;//22.6942072709,114.3524087439
var longitude = 22.6942072709;

var center = [latitude,longitude];

/*============================地形图层================================*/
var normal_background = new appLayer({
	urls: ['http://t0.tianditu.com/DataServer?T=vec_w&x={x}&y={y}&l={z}',
	        'http://t1.tianditu.com/DataServer?T=vec_w&x={x}&y={y}&l={z}',
			'http://t2.tianditu.com/DataServer?T=vec_w&x={x}&y={y}&l={z}',
			'http://t3.tianditu.com/DataServer?T=vec_w&x={x}&y={y}&l={z}',
			'http://t4.tianditu.com/DataServer?T=vec_w&x={x}&y={y}&l={z}',
			'http://t5.tianditu.com/DataServer?T=vec_w&x={x}&y={y}&l={z}',
			'http://t6.tianditu.com/DataServer?T=vec_w&x={x}&y={y}&l={z}',
			'http://t7.tianditu.com/DataServer?T=vec_w&x={x}&y={y}&l={z}'],
	mapExtent: [-2.0037508342787E7, -2.0037508342787E7, 2.0037508342787E7, 2.0037508342787E7],
	tilePixelRatio: 1,
	fromProject: "EPSG:102100",
	toProject: "EPSG:3857"
})

var normal_data = new appLayer({
	urls: ['http://t0.tianditu.com/DataServer?T=cva_w&x={x}&y={y}&l={z}',
	        'http://t1.tianditu.com/DataServer?T=cva_w&x={x}&y={y}&l={z}',
			'http://t2.tianditu.com/DataServer?T=cva_w&x={x}&y={y}&l={z}',
			'http://t3.tianditu.com/DataServer?T=cva_w&x={x}&y={y}&l={z}',
			'http://t4.tianditu.com/DataServer?T=cva_w&x={x}&y={y}&l={z}',
			'http://t5.tianditu.com/DataServer?T=cva_w&x={x}&y={y}&l={z}',
			'http://t6.tianditu.com/DataServer?T=cva_w&x={x}&y={y}&l={z}',
			'http://t7.tianditu.com/DataServer?T=cva_w&x={x}&y={y}&l={z}'],
	mapExtent: [-2.0037508342787E7, -2.0037508342787E7, 2.0037508342787E7, 2.0037508342787E7],
	tilePixelRatio: 1,
	fromProject: "EPSG:102100",
	toProject: "EPSG:3857"
})


var arrNormal = new ol.Collection();
arrNormal.push(normal_background);
arrNormal.push(normal_data);

var normal_group = new ol.layer.Group({
	//mapType: ol.control.MapType.NORMAL_MAP,
	layers : arrNormal
});

var attribution = new ol.control.Attribution({
	className : 'none'
});

/*============================矢量图层================================*/
var vector_background = new ol.layer.Vector({
  source: new ol.source.Vector({
    url: function(extent, resolution, projection){
		var topRight = ol.proj.transform(ol.extent.getTopRight(extent),'EPSG:3857', 'EPSG:4326');
		var bottomLeft = ol.proj.transform(ol.extent.getBottomLeft(extent),'EPSG:3857', 'EPSG:4326');
		var tUrl = "/gis/getGeom?left=" + bottomLeft[0] + '&top=' + bottomLeft[1] +
   		                    '&right=' + topRight[0] + "&bottom=" + topRight[1]+"&layerName=dlzxc"; 
        //var tUrl = "china.json";  							  
		return tUrl;
	},
	//strategy : 加载策略
	//目标是从数据源请求矢量的方式，包括单次请求全部元素 ol.loadingstrategy.all,默认
	//当前视图范围 ol.loadingstrategy.bbox
	//切片范围 ol.loadingststrategy.tile
	strategy: ol.loadingstrategy.bbox,
	//strategy: ol.loadingstrategy.all,
    format: new ol.format.GeoJSON({
        extractStyles: false
    })
  })
});

var map = new ol.Map({
	view: new ol.View({
		center:  new ol.proj.transform(center,"EPSG:4326","EPSG:3857"),
		maxZoom : 23,
		minZoom : 13,
		zoom: 13
	}),
	controls: ol.control.defaults({ attribution: false }).extend([attribution]),
	target:"map"
});


map.addLayer(normal_group);
map.addLayer(vector_background);

var mousePosition = new ol.control.MousePosition({
    coordinateFormat: ol.coordinate.createStringXY(5),
    projection: 'EPSG:4326',
    target: document.getElementById('myposition'),
    undefinedHTML: '&nbsp;'
    });

map.addControl(mousePosition);



ol.layer.SXZDT = function(opt_options) {
	
	var options = opt_options || {};
	this.source_ = new ol.source.Vector();
	this.layerName_ = options.layerName ? options.layerName : '';
	this.name_ = options.name ? options.name : '';
  
	this.maxZoom = options.maxZoom ? options.maxZoom : -1;
	this.minZoom = options.minZoom ? options.minZoom : -1;
	
	this.visible = true;
	
	var this_ = this;
	ol.layer.Vector.call(this, {
		source : this_.source_,
		style : new ol.style.Style({
			stroke: new ol.style.Stroke({
				color: '#7F7F7F',
				width: 1
		    })
		})
	});
	
	var myExtent = map.getView().calculateExtent(map.getSize());
    var bottomLeft = ol.proj.transform(ol.extent.getBottomLeft(myExtent),'EPSG:3857', 'EPSG:4326');
    var topRight = ol.proj.transform(ol.extent.getTopRight(myExtent),'EPSG:3857', 'EPSG:4326');
    
    $.ajax({
        url: '/map/getGeom',
        data: "left=" + bottomLeft[0] + "&top=" + bottomLeft[1] + "&right=" + topRight[0] + "&bottom=" + topRight[1] + "&layerName="+this_.layerName_,
        type: 'POST',
        success: function(res){
            //var geojsonObject = Ext.util.JSON.decode(res);
            var features = (new ol.format.GeoJSON()).readFeatures(res);
            this_.source_.clear(true);
            this_.source_.addFeatures(features);
            //this_.dimTexts = geojsonObject.dimTexts;
        }
    });
	
}
ol.inherits(ol.layer.SXZDT, ol.layer.Vector);

ol.layer.SXZDT.prototype.setMap = function(map) {
        ol.layer.Vector.prototype.setMap.call(this, map);
		var this_ = this;
		map.on('moveend',function(e){
              this_.refreshSource_(e);
		});
		
};

ol.layer.SXZDT.prototype.refreshSource_ = function(e) {
	        var current_zoom = map.getView().getZoom();
			var visible = true;
			if(this.maxZoom != -1 && this.minZoom != -1) {
				if(current_zoom >= this.minZoom && current_zoom <= this.maxZoom)
					visible = true;
				else
					visible = false;
		    }
		    else if(this.maxZoom != -1 && this.minZoom == -1) {
				   if(current_zoom <= this.maxZoom)
					 visible = false;
				else
					visible = true;
		    }
		    else if(this.minZoom != -1 && this.maxZoom == -1) {
					if(current_zoom >= this.minZoom)
					  visible = true;
				else
					  visible = false;
		    }
            var this_ = this;
            if(this.visible & visible) {
				var myExtent = map.getView().calculateExtent(map.getSize());
				var bottomLeft = ol.proj.transform(ol.extent.getBottomLeft(myExtent),'EPSG:3857', 'EPSG:4326');
				var topRight = ol.proj.transform(ol.extent.getTopRight(myExtent),'EPSG:3857', 'EPSG:4326');
				
				$.ajax({
					url: 'getGeom',
					data: "left=" + bottomLeft[0] + "&top=" + bottomLeft[1] + "&right=" + topRight[0] + "&bottom=" + topRight[1] + "&layerName="+this_.layerName_,
					type: 'POST',
					success: function(res){
						//var geojsonObject = Ext.util.JSON.decode(res);
						var features = (new ol.format.GeoJSON()).readFeatures(res);
						this_.source_.clear(true);
						this_.source_.addFeatures(features);
						//this_.dimTexts = geojsonObject.dimTexts;
					}
				});
				this.setVisible(true);
			}
			else{
				this.dimTexts = null;
				this.setVisible(false);
				this.source_.clear(true);
			}
}

//dlzxc
var dlzxc_layer = new ol.layer.SXZDT({
	layerName : 'dlzxc',
	name:'道路中线层',
	minZoom : 13
});

var layers1 = new ol.Collection();
layers1.push(dlzxc_layer);

var layer_group = new ol.layer.Group({
    layers:layers1
});
map.addLayer(layer_group);
//dlzxc_layer.setMap(map);
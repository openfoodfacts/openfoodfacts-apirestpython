queue()
    .defer(d3.json, "/products/stats/date?dateby=1")
    .await(makeGraphs);

function makeGraphs(error, productsJSON, statesJson) {
	
	//Clean productsJSON data
	var products = productsJSON;
	var dateFormat = d3.time.format("%Y-%m");
	products.forEach(function(d) {
		var dateyear = d["dateyear"];
		var datemonth = d["datemonth"];
		d["date"] = dateFormat.parse(dateyear + '-' + datemonth);
	});

	//Create a Crossfilter instance
	var ndx = crossfilter(products);

	//Define Dimensions
	var dateDim = ndx.dimension(function(d) { return d["date"]; });


	//Calculate metrics
	var numProductsByDate = dateDim.group().reduceSum(function(d){return d.count;});; 

	var all = ndx.groupAll();

	//Define values (to be used in charts)
	var minDate = dateDim.bottom(1)[0]["date"];
	var maxDate = dateDim.top(1)[0]["date"];

    //Charts
	var timeChart = dc.lineChart("#time-chart");

	timeChart
		.width(700)
		.height(300)
		.margins({top: 10, right: 50, bottom: 30, left: 50})
		.dimension(dateDim)
		.group(numProductsByDate)
		.transitionDuration(500)
		.x(d3.time.scale().domain([minDate, maxDate]))
		.xUnits(d3.time.month)
		.elasticY(true)
		.yAxis().ticks(4);

    dc.renderAll();

};
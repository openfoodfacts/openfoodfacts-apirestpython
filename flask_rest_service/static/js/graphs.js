queue()
    .defer(d3.json, "/products/stats/date?dateby=1")
    .await(makeGraphs);

function makeGraphs(error, productsJSON, statesJson) {
	
	//Clean productsJSON data
	var products = productsJSON;
	var dateFormat = d3.time.format("%Y-%m");
	var totalProd = 0;
	products.forEach(function(d) {
		var dateyear = d["dateyear"];
		var datemonth = d["datemonth"];
		d["date"] = dateFormat.parse(dateyear + '-' + datemonth);
		totalProd += d['count'];
	});

	//Create a Crossfilter instance
	var ndx = crossfilter(products);

	//Define Dimensions
	var dateDim = ndx.dimension(function(d) { return d["date"]; });
	var numberProductsDim = ndx.dimension(function(d) { return d["count"]; });


	//Calculate metrics
	var numProductsByDate = dateDim.group().reduceSum(function(d){return d.count;});

	var all = ndx.groupAll();
	var totalProducts = ndx.groupAll().reduceSum(function(d) {return d["count"];});

	//Define values (to be used in charts)
	var minDate = dateDim.bottom(1)[0]["date"];
	var maxDate = dateDim.top(1)[0]["date"];

    //Charts
	var timeChart = dc.lineChart("#time-chart");
	var productsDisp = dc.numberDisplay("#number-products");
	var totalProductsDisp = document.getElementById('number-products-total');
	var dateRange = document.getElementById('date-range');
	totalProductsDisp.innerText = totalProd;

	productsDisp
		.formatNumber(d3.format("d"))
		.valueAccessor(function(d){return d; })
		.group(totalProducts)

	timeChart
		.width(680)
		.height(300)
		.margins({top: 10, right: 10, bottom: 20, left: 40})
		.dimension(dateDim)
		.group(numProductsByDate)
		.renderlet(function(chart){
		    dc.events.trigger(function(){
		    	var firstDateNonParsed = timeChart.brush().extent()[0].toISOString().split('T')[0];
		    	var lastDateNonParsed = timeChart.brush().extent()[1].toISOString().split('T')[0];
		    	if(firstDateNonParsed == '2012-01-01' && lastDateNonParsed == '2012-01-01') {
		    		lastDateNonParsed = dateDim.top(1)[0]["date"].toISOString().split('T')[0];
		    	}
		        dateRange.innerText = firstDateNonParsed + ' / ' + lastDateNonParsed;
		    });
		})
		.renderArea(true)
		.transitionDuration(500)
		.x(d3.time.scale().domain([minDate, maxDate]))
		.xUnits(d3.time.month)
		.elasticY(true);

    dc.renderAll();

};
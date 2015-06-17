queue()
    .defer(d3.json, "/products/stats/info?dateby=1")
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
		if(!d['saltlevels']) d['saltlevels'] = 'undifined';
		if(!d['fatlevels']) d['fatlevels'] = 'undifined';
		if(!d['saturatedfatlevels']) d['saturatedfatlevels'] = 'undifined';
		if(!d['sugarslevels']) d['sugarslevels'] = 'undifined';
	});

	//Create a Crossfilter instance
	var ndx = crossfilter(products);

	//Define Dimensions
	var dateDim = ndx.dimension(function(d) { return d["date"]; });
	var numberProductsDim = ndx.dimension(function(d) { return d["count"]; });
	var saltLevelsProductsDim = ndx.dimension(function(d) { return d["saltlevels"]; });
	var fatLevelsProductsDim = ndx.dimension(function(d) { return d["fatlevels"]; });
	var saturatedFatLevelsProductsDim = ndx.dimension(function(d) { return d["saturatedfatlevels"]; });
	var sugarsLevelsProductsDim = ndx.dimension(function(d) { return d["sugarslevels"]; });

	//Calculate metrics
	var numProductsByDate = dateDim.group().reduceSum(function(d){return d.count;});
	var numProductsSaltLevels = saltLevelsProductsDim.group().reduceSum(function(d){return d.count;});
	var numProductsFatLevels = fatLevelsProductsDim.group().reduceSum(function(d){return d.count;});
	var numProductsSaturedFatLevels = saturatedFatLevelsProductsDim.group().reduceSum(function(d){return d.count;});
	var numProductsSugarsLevels = sugarsLevelsProductsDim.group().reduceSum(function(d){return d.count;});

	var all = ndx.groupAll();
	var totalProducts = ndx.groupAll().reduceSum(function(d) {return d["count"];});

	//Define values (to be used in charts)
	var minDate = dateDim.bottom(1)[0]["date"];
	var maxDate = dateDim.top(1)[0]["date"];

    //Charts
	var timeChart = dc.lineChart("#time-chart");
	var saltChart = dc.rowChart("#salt-levels");
	var fatChart = dc.rowChart("#fat-levels");
	var sugarsChart = dc.rowChart("#sugars-levels");
	var saturedFatChart = dc.rowChart("#saturated-fat-levels");
	var productsDisp = dc.numberDisplay("#number-products");
	var totalProductsDisp = document.getElementById('number-products-total');
	var dateRange = document.getElementById('date-range');
	totalProductsDisp.innerText = totalProd;

	productsDisp
		.formatNumber(d3.format("d"))
		.valueAccessor(function(d){return d; })
		.group(totalProducts);

	saltChart
	    .width(300)
	    .height(250)
	    .dimension(saltLevelsProductsDim)
	    .group(numProductsSaltLevels)
	    .xAxis().ticks(4);
	    
	saturedFatChart
	    .width(300)
	    .height(250)
	    .dimension(saturatedFatLevelsProductsDim)
	    .group(numProductsSaturedFatLevels)
	    .xAxis().ticks(4);

	fatChart
	    .width(300)
	    .height(250)
	    .dimension(fatLevelsProductsDim)
	    .group(numProductsFatLevels)
	    .xAxis().ticks(4);

	sugarsChart
	    .width(300)
	    .height(250)
	    .dimension(numProductsSugarsLevels)
	    .group(numProductsSugarsLevels)
	    .xAxis().ticks(4);

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
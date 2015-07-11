
	function drawsplot(filename) {

    // var data = [[5,3], [10,17], [15,4], [2,8]];
    var data;

    //var cValue = function(d) { if (d.weight > 0) return d.weight*2 + 8 ; else return 0;};
    var fill = d3.scale.category20();
	
	var filename1 = filename+'splot1.json';
	var filename2 = filename+'splot2.json';
	
	
    d3.json(filename1, function(error, json) {
      //if (error) return console.warn(error);
      data = json;
 
	d3.layout.cloud().size([1200, 900])
      .words(data.map(function(d) {
        return {text: d.word, size: d.weight};
      }))
      .padding(5)
      .rotate(function() { return ~~(Math.random() * 2) * 90; })
      .font("Impact")
      .fontSize(function(d) { return d.size; })
      .on("end", draw1)
      .start();

  function draw1(words) {
  
		var	margin = {top: 30, right: 20, bottom: 30, left: 50},
			width = 900 - margin.left - margin.right,
			height = 500 - margin.top - margin.bottom;

  
		var chart1 = d3.select("body").append("svg").attr("id","splot1").attr("width", 900)
        .attr("height", 500).append("g")
        .attr("transform", "translate(500,300)");
		
      chart1
      .selectAll("text")
        .data(words)
      .enter().append("text")
        .style("font-size", function(d) { if (d.size < 2) return (0)
                            .toString().concat("px"); else if (d.size < 6) return  (d.size*3 + 5).toString().concat("px") ; else if (d.size < 20) return  (d.size*2 + 8).toString().concat("px") ; else return "50px"  })
        .style("font-family", "Impact")
        .style("fill", function(d, i) { return fill(i); })
        .attr("text-anchor", "middle")
        .attr("transform", function(d) {

          return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
        })
        .text(function(d) { return d.text; });
		//.on("click", function(d) {alert(d.text);});
		
		
		
		chart1.append("text")
        .attr("x", 0)             
        .attr("y", -275)
        .attr("text-anchor", "middle")  
        .style("font-size", "32px") 
        .style("text-decoration", "underline")  
        .text("Positive Tweets");
		
		var rectangle = chart1.append("rect")
                             .attr("x", -360)
                             .attr("y", -260)
                            .attr("width", 700)
                            .attr("height", 460)
							.attr("fill", "transparent")
							.style("stroke-width",1)
							.style("stroke", "black");	


  }
  });
  
  
  d3.json(filename2, function(error, json) {
      //if (error) return console.warn(error);
      data = json;
 
	d3.layout.cloud().size([1200, 900])
      .words(data.map(function(d) {
        return {text: d.word, size: d.weight};
      }))
      .padding(5)
      .rotate(function() { return ~~(Math.random() * 2) * 90; })
      .font("Impact")
      .fontSize(function(d) { return d.size; })
      .on("end", draw2)
      .start();

  function draw2(words) {
  
		var	margin = {top: 30, right: 20, bottom: 30, left: 50},
			width = 900 - margin.left - margin.right,
			height = 500 - margin.top - margin.bottom;

  
		var chart2 = d3.select("body").append("svg").attr("id","splot2").attr("width", 900)
        .attr("height", 500).append("g")
        .attr("transform", "translate(500,300)");
		
      chart2
      .selectAll("text")
        .data(words)
      .enter().append("text")
        .style("font-size", function(d) { if (d.size < 2) return (0)
                            .toString().concat("px"); else if (d.size < 6) return  (d.size*3 + 5).toString().concat("px") ; else if (d.size < 20) return  (d.size*2 + 8).toString().concat("px") ; else return "50px"  })
        .style("font-family", "Impact")
        .style("fill", function(d, i) { return fill(i); })
        .attr("text-anchor", "middle")
        .attr("transform", function(d) {

          return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
        })
        .text(function(d) { return d.text; });
		//.on("click", function(d) {alert(d.text);});
		
		
		
		chart2.append("text")
        .attr("x", 0)             
        .attr("y", -275)
        .attr("text-anchor", "middle")  
        .style("font-size", "32px") 
        .style("text-decoration", "underline")  
        .text("Negative Tweets");
		
		var rectangle = chart2.append("rect")
                             .attr("x", -360)
                             .attr("y", -260)
                            .attr("width", 700)
                            .attr("height", 460)
							.attr("fill", "transparent")
							.style("stroke-width",1)
							.style("stroke", "black");	
  }
  });
};
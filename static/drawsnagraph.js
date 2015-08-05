
	function drawsnagraph(filename) {
		
		var	margin = {top: 50, right: 20, bottom: 30, left: 50},
			width = 1300 - margin.left - margin.right,
			height = 700 - margin.top - margin.bottom;


		var color = d3.scale.category20();

		var force = d3.layout.force()
			.charge(function(d) { if (d.weight < 3) return -70 ; else if (d.weight < 7) return -160;  else return -d.weight * d.weight - 150 ; })
			.linkStrength(1)  //1
			.linkDistance(function(d) { return 10*d.weight + 50; })
			.size([width, height]);

		var link, node;	
		
		d3.json(filename, function(error, graph) {
		  force
			  .nodes(graph.nodes)
			  .links(graph.links)
			  .start();
		
		var div = d3.select("body")
			.append("div")	//declare the tooltip div
			.attr("class", "tooltip")	//apply the 'tooltip' class
			.attr("id", "idtooltip")
			.style("opacity", 0)
			.attr("onclick","$(this).fadeTo('fast',0.1);");
		
		var svg = d3.select("body").append("svg")
		.attr("id","snagraph")
		.attr("width", width + margin.left + margin.right)
		.attr("height", height + margin.top + margin.bottom)
		.append("g")
			.attr("transform", "translate(" + margin.left + "," + margin.top + ")");
		
			//.attr("width", width)
			//.attr("height", height);

		var rectangle = svg.append("rect")
                             .attr("x", margin.left)
                             .attr("y", -margin.top)
                            .attr("width", 1300 - 2*margin.left - margin.right)
                            .attr("height", 700)
							.attr("fill", "white")
							.style("stroke-width",1)
							.style("stroke", "black");

		   link = svg.selectAll(".link")
			  .data(graph.links)
			.enter().append("line")
			  .attr("class", "link")
			  .style("stroke-width", function(d) { return Math.sqrt(d.weight); });

			//link.exit().remove();
		
			// Define the line
		//var	tip = if (d.tweet != null) return d.tweet; else return d.screen_name;;
			  
		  node = svg.selectAll(".node")
				.data(graph.nodes)
				.enter().append("circle")
				.attr("class", "node")
				.attr("r", function(d) { if ((d.weight > 0) && (d.weight <= 20)) return d.weight*2 + 5 ; else if (d.weight > 20) return 60;  else return 0; })
				.style("fill", function(d) { return color(d.weight); })
				.call(force.drag)
				.on("mousedown", function(d){
					//div.transition()
					//	.duration(500)
					//	.style("opacity", 0);
					div.transition()
						.duration(200)
						.style("opacity", .9)
						.style("display","block");
					if (d.tweet != null) 
						{ var tip=d.tweet; var tiplen="125px"; var tipwidth="150px";} 
					else  
						{tip=d.screen_name; tiplen="30px"; tipwidth=d.screen_name.length+75+"px";}
					div.html(
						'<a href="https://twitter.com/' + d.screen_name+'" target="_blank">' +
						'<u>' + d.screen_name +
						'</u></a><br/><br/><p>' + tip +'</p>')
						.style("height", tiplen)
						.style("width", tipwidth)
						.style("left", (d3.event.pageX) + "px")
						.style("top", (d3.event.pageY - 25) + "px");
				});

		  node.append("title")
			  .text(function(d) { if (d.tweet != null) return d.tweet; else return d.screen_name; });

		  var texts = svg.selectAll("text.label")
						.data(graph.nodes)
						.enter().append("text")
						.attr("class", "label")
						.attr("fill", "black")
						.style("font-size", function(d) { if (d.weight < 10 ) return (d.weight*2 + 5)
                            .toString().concat("px"); else if (d.weight < 20) return "25px" ; else return "40px" })
						.text(function(d) {  if (d.weight > 1) return d.screen_name;  });


		  force.on("tick", function() {
			link.attr("x1", function(d) { return d.source.x; })
				.attr("y1", function(d) { return d.source.y; })
				.attr("x2", function(d) { return d.target.x; })
				.attr("y2", function(d) { return d.target.y; });

			node.attr("cx", function(d) { return d.x; })
				.attr("cy", function(d) { return d.y; });

			texts.attr("transform", function(d) {
				return "translate(" + d.x + "," + d.y + ")"; });

		  });

		});

		};
		
		//drawsnagraph();
		
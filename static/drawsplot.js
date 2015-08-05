
	function drawsplot(filename) {

    // var data = [[5,3], [10,17], [15,4], [2,8]];
    var data;

    //var cValue = function(d) { if (d.weight > 0) return d.weight*2 + 8 ; else return 0;};
    var fill = d3.scale.category20();
	
	var filename1 = filename+'splot1.json';
	var filename2 = filename+'splot2.json';


	console.log(filename1);
	console.log("declared filename and before calling d3json for WordCloud");
	
// code for positive sentiment word cloud	
    d3.json(filename1, function(error, json) {
      //if (error) return console.warn(error);
      data = json;
		//alert(data.length);
		
		var el = document.getElementById('positiveTweetCount');
			el.innerHTML = '<h3>'+data.length+' Distinct Words!</h3>';
		WordCloud(document.getElementById('cloudp'), {	
		  gridSize: 12, 
		  weightFactor: 2, 
		  rotateRatio: 0.5,
		  //list : tags.map(function(word) { return [word[0], Math.round(word[1]/5)]; }), 
		  list : data, 
		  //list : [["Gerald",34],["Philo",30],["Elaine",4]], 
		  wait: 1
		});
		
  });

	console.log("before calling d3json for negative sentiment");

  
  // code for negative sentiment word cloud
    d3.json(filename2, function(error, json) {
      //if (error) return console.warn(error);
      data = json;
		//alert(data.length);
		var el = document.getElementById('negativeTweetCount');
			el.innerHTML = '<h3>'+data.length+' Distinct Words!</h3>';
		WordCloud(document.getElementById('cloudn'), {	
		  gridSize: 12, 
		  weightFactor: 2, 
		  rotateRatio: 0.5,
		  list : data, 
		  wait: 5
		});
		
  });

	console.log("after calling d3json for negative sentiment");
};
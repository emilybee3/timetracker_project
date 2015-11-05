
      var margin = { top: 50, right: 100, bottom: 100, left: 70},
          width = 960 - margin.left - margin.right,
          height = 960 - margin.top - margin.bottom,
          gridSize = Math.floor(width / 12), //how big the grid appears in the window
          legendElementWidth = gridSize + 10,
          buckets = 9, //catagories to split data into
          colors = ["red","yellow","green"], // alternatively colorbrewer.YlGnBu[9]
          days = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"],
          times = ["6a - 8a", "2a", "3a", "4a", "5a", "6a", "7a", "8a", "9a", "10a", "11a", "12a", "1p", "2p", "3p", "4p", "5p", "6p", "7p", "8p", "9p"];
          datasets = ["data.tsv", "data2.tsv", "data3.tsv"];

      var svg = d3.select("#chart").append("svg") //makes chart 
          .attr("width", width + margin.left + margin.right)
          .attr("height", height + margin.top + margin.bottom)
          .append("g") //?
          .attr("transform", "translate(" + margin.left + "," + margin.top + ")");//puts chart inside of the margins

      var dayLabels = svg.selectAll(".dayLabel") //adds day lables 
          .data(days)
          .enter().append("text")
            .text(function(d) { return d; })
            .attr("x", function(d, i) { return i * gridSize * 2; })// changes spacing
            .attr("y", 0)
            .style("text-anchor", "middle")
            .attr("transform", "translate(" + gridSize / 2 + ", -6)")
            .attr("class", function (d, i) { return ((i >= 0 && i <= 4) ? "dayLabel mono axis axis-workweek" : "dayLabel mono axis"); });

      var timeLabels = svg.selectAll(".timeLabel") //adds time lables
          .data(times)
          .enter().append("text")
            .text(function (d) { return d; })
            .attr("x", 0)
            .attr("y", function (d, i) { return i * gridSize * 2; })//changes spacing
            .style("text-anchor", "end")
            .attr("transform", "translate(-6," + gridSize / 1.5 + ")")
            .attr("class", function(d, i) { return ((i >= 7 && i <= 16) ? "timeLabel mono axis axis-worktime" : "timeLabel mono axis"); });


/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


      var heatmapChart = function() { //makes objects from data
        d3.json("/sendjson",
        function(data) {

//           //THIS FUNCTION MAKES SVG CARDS FOR EACH .HOUR


          var cards = svg.selectAll(".hour")
              .data(data.data, function(d){return d.day+":"+d.hour;});
              
              //select all .hours and make a card for each

          cards.append("title");//gives cards a title so they can be edited later?

          cards.enter().append("rect") //puts svg rectangle for each card
              .attr("y", function(d) { return (d.hour - 1) * (gridSize *2); })
              .attr("x", function(d) { return (d.day - 1) * (gridSize *2); })
              .attr("rx", 1)
              .attr("ry", 1)
              .attr("class", "hour bordered")
              .attr("id", "card")
              .attr("width", gridSize * 2)
              .attr("height", gridSize)
              .style("fill", function(d) {return d.value});

          // cards.append("text").text(function(d) { return d.words; })

          cards.transition().duration(1000)
              .style("fill", function(d) { return d.value; }); //assigns color to cards

          cards.select("title").text(function(d) { return d.value; });//turns cards the color of their value
////////////////////////////////////////////////////////////////////////////////
          var cardsgroup = cards.append("g");

          console.log(cards)
        // var bounds = d3.select('cards');
        var bounds = {
        x:10,  // bounding box is 300 pixels from the left
        y:11, // bounding box is 400 pixels from the top
        width: 500, // bounding box is 500 pixels across
        height: 600 // bounding box is 600 pixels tall
    };
        
    
           //creates group element for all cards

          var timespent = svg.selectAll(".card") //adds words lables
                    .data(data.data)
                    .enter().append("text")
                      .text(function(d) { return d.words; })
                      .attr("y", function(d) { return (d.hour - 1) * gridSize * 2 + 10; })
                      .attr("x", function(d) { return (d.day - 1) * gridSize * 2+ 10; })
                      .style("text-anchor", "middle")
                      .attr("id", "words")

          //             // .call(wrap, 200)

          //             console.log(timespent)

        // var bounds = d3.select('rect#card');
        // console.log(bounds)
        d3.select('text#words').textwrap(bounds);


////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
  /////these endings close the heatmap function 
       });
        };
/////////////////////////////////////////////////////////////////////////////////////
// function wrap(text, width) {
//     text.each(function () {
//         var text = d3.select(this),
//             words = text.text().split(/\s+/).reverse(),
//             word,
//             line = [],
//             lineNumber = 0,
//             lineHeight = 1.1, // ems
//             x = text.attr("x"),
//             y = text.attr("y"),
//             dy = 0, //parseFloat(text.attr("dy")),
//             tspan = text.text(null)
//                         .append("tspan")
//                         .attr("x", x)
//                         .attr("y", y)
//                         .attr("dy", dy + "em");
//         while (word = words.pop()) {
//             line.push(word);
//             tspan.text(line.join(" "));
//             if (tspan.node().getComputedTextLength() > width) {
//                 line.pop();
//                 tspan.text(line.join(" "));
//                 line = [word];
//                 tspan = text.append("tspan")
//                             .attr("x", x)
//                             .attr("y", y)
//                             .attr("dy", ++lineNumber * lineHeight + dy + "em")
//                             .text(word);

//             }
//         }
//     });
// }
      heatmapChart();
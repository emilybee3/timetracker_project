
      var margin = { top: 50, right: 100, bottom: 100, left: 70},
          width = 2000 - margin.left - margin.right,
          height = 1450 - margin.top - margin.bottom,
          gridSize = Math.floor(width / 20), //how big the grid appears in the window
          legendElementWidth = gridSize + 10,
          buckets = 9, //catagories to split data into
          colors = ["red","yellow","green"], // alternatively colorbrewer.YlGnBu[9]
          days = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"],
          times = ["6a - 8a", "8a - 9a", "9a - 10a", "10a - 11a", "11a - 12p", "12p - 1p", "1p - 2p", "2p - 3p", "3p - 4p", "4p - 5p", "5p - 6p", "6p - 7p", "7p - 8p", "8p - 9p", "9p - 12p"];

      var svg = d3.select("#chart").append("svg") //makes chart 
          .attr("width", width + margin.left + margin.right)
          .attr("height", height + margin.top + margin.bottom)
          .append("g") //?
          .attr("transform", "translate(" + margin.left + "," + margin.top + ")");//puts chart inside of the margins

      var dayLabels = svg.selectAll(".dayLabel") //adds day lables 
          .data(days)
          .enter().append("text")
            .text(function(d) { return d; })
            .attr("x", function(d, i) { return i * gridSize * 2.2; })// changes spacing
            .attr("y", 0)
            .style("text-anchor", "middle")
            .attr("transform", "translate(" + gridSize / 2 + ", -6)")
            .attr("class", function (d, i) { return ((i >= 0 && i <= 4) ? "dayLabel mono axis axis-workweek" : "dayLabel mono axis"); });

      var timeLabels = svg.selectAll(".timeLabel") //adds time lables
          .data(times)
          .enter().append("text")
            .text(function (d) { return d; })
            .attr("x", 0)
            .attr("y", function (d, i) { return i * gridSize; })//changes spacing
            .style("text-anchor", "end")
            .attr("transform", "translate(-6," + gridSize / 1.5 + ")")
            .attr("class", function(d, i) { return ((i >= 7 && i <= 16) ? "timeLabel mono axis axis-worktime" : "timeLabel mono axis"); });


/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


      var heatmapChart = function() { //makes objects from data
        d3.json("/sendjson",
        function(data) {
          console.log(data);

//           //THIS FUNCTION MAKES SVG CARDS FOR EACH .HOUR


          var cards = svg.selectAll(".hour")
              .data(data.data, function(d){return d.day+":"+d.hour;})
              .enter().append("g");    
              //select all .hours and make a card for each

          

          cards.append("rect") //puts svg rectangle for each card
              .attr("y", function(d) { return (d.hour - 1) * (gridSize); })
              .attr("x", function(d) { return (d.day - 1) * (gridSize *2); })
              .attr("rx", 1)
              .attr("ry", 1)
              .attr("class", "hour bordered")
              .attr("id", function(d) { return ("card" + d.response_id);})
              .attr("width", gridSize * 2)
              .attr("height", gridSize)
              .style("fill", function(d) {return d.value});


          cards.transition().duration(1000)
              .style("fill", function(d) { return d.value; }); //assigns color to cards

          cards.select("title").text(function(d) { return d.value; });//turns cards the color of their value
////////////////////////////////////////////////////////////////////////////////

          console.log(cards)


          // var timespent = svg.selectAll(".card") //adds words lables
                    // .data(data.data)
                    // .enter()

                    cards.append("text")
                      .text(function(d) {  
                        return d.words; })
                      .attr("y", function(d) { return (d.hour - 1) * gridSize * 2 + 10; })
                      .attr("x", function(d) { return (d.day - 1) * gridSize * 2+ 10; })
                      .style("text-anchor", "middle")
                      .attr("id", function(d){ return ("words" + d.response_id);});//setting id to be the rsponse id and string word

        cards[0].forEach(function(card){ 
          var responseId = card.__data__.response_id;
          var correspondingRectangle = d3.select("#card" + responseId);//grabbing the words to be changed by id
          d3.select("#words" + responseId).textwrap(correspondingRectangle, 5);
        });
       
        


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
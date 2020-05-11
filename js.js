var initMap = function(accidents) {
    var map = new google.maps.Map(d3.select("#map").node(), {
        zoom: 3,
        center: new google.maps.LatLng(40, -99),
        mapTypeId: google.maps.MapTypeId.TERRAIN
    });
    
    createOverlay(map, accidents);
    
    // Create the event to add the city names when zooming in
    google.maps.event.addListener(map, 'zoom_changed', function() {
        // If we're in close enough, show the city name
        if(map.getZoom() >= 6) {
            d3.selectAll(".label").classed("hidden", false);
        } else if(map.getZoom() < 6) {
            // Hide the city name when zooming out
            d3.selectAll(".label").classed("hidden", true);
        }
    });
}

var createOverlay = function(map, data) {
    // Create the overlay that we are to draw
    var overlay = new google.maps.OverlayView();
    
    // When adding the overlay, create the container for the points
    overlay.onAdd = function() {
        // Put this container within the layer for the overlay
        // From the documentation, we use the overlayMouseTarget layer to accept mouse events
        var layer = d3.select(this.getPanes().overlayMouseTarget).append("div")
                      .classed("accidents", true);

        // Draw the overlay
        overlay.draw = function() {
            // Get the projection for this layer and set the padding
            var projection = this.getProjection(),
            padding = 10;

            // Create an SVG element for each marker
            var marker = layer.selectAll("svg")
                                .data(data)
                                .style("left", function(accident) {
                                    accident = new google.maps.LatLng(accident.lat, accident.long);
                                    accident = projection.fromLatLngToDivPixel(accident);
                                    
                                    return (accident.x - padding) + "px";
                                })
                                .style("top", function(accident) {
                                    accident = new google.maps.LatLng(accident.lat, accident.long);
                                    accident = projection.fromLatLngToDivPixel(accident);
                                    
                                    return (accident.y - padding) + "px";
                                })
                              .enter()
                                .append("svg")
                                .attr("class", "marker")
                              
                    .on("mouseover", function(accident) {
                        d3.select("#ac-type")
                            .text(accident.manmo);
                        d3.select("#location")
                            .text(accident.location);
                        d3.select("#date")
                            .text(accident.date);
                        d3.select("#ntsb")
                            .text(accident.ntsbID);
                        d3.select("#injury")
                            .text(accident.injuries.totalInjuredEXCFatalities);
                        d3.select("#fatal")
                            .text(accident.injuries.fatal);
                
                        // Show the tooltip in relation to the mouse
                        //var mouse = d3.mouse(d3.select("body"));
                        //console.log(mouse);
                        
                        d3.select("#tooltip").classed("hidden", false).style("left", d3.event.pageX).style("top", d3.event.pageY);
                    })
                    .on("mouseout", function() {
                        d3.select("#tooltip").classed("hidden", true);
                    });

            // Draw the circle for the marker
            marker.append("circle")
                    .attr("r", 6)
                    .attr("cx", padding)
                    .attr("cy", padding)
                    .attr("fill", function(accident) {
                        if(accident.injuries.fatal > 0) {
                            return "black";
                        } else {
                            return "gray";
                        }
                    })
                    .attr("stroke", function(accident) {
                        if(accident.timeOfYear == "summer") {
                            return "blue";
                        } else if(accident.timeOfYear == "fall") {
                            return "yellow";
                        } else if(accident.timeOfYear == "winter") {
                            return "gray";
                        } else {
                            return "green";
                        }
                    });

            // Show the location along with the circle
            marker.append("text")
                    .attr("x", padding + 7)
                    .attr("y", padding)
                    .classed("label", true).classed("hidden", true)
                    .text(function(accident) { return accident.location; });
        };
    }
    
    // Tell the map what to do when removing the layer
    overlay.onRemove = function() {
        d3.select(".accidents").remove();
    }
    
    overlay.setMap(map);
}

d3.json("data/allData.json").then(function(data) {
    data = data.data
    initMap(data);
}, function(error) {
      console.log("error"+error);
})
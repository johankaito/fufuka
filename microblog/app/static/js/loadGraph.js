//Get kafka topics


//Get the latest JMX data
    setInterval(function(){
   function obtainedResult(data) {
        console.log(data);
    }
    $.ajax({
        url: "http://127.0.0.1:8778/jolokia/read/kafka.server:type=BrokerTopicMetrics,name=MessagesInPerSec,topic=*",
        type: "get",
        datatype:"json",        
        success: function(response){
        // Execute our callback function
        obtainedResult(response);
}
});

    }, 1000);

// http://blog.thomsonreuters.com/index.php/mobile-patent-suits-graphic-of-the-day/
var topics = {{ topics }};
var links = {{ json_data }};
var nodes = {};

//Position the rootnode
var rootX = 10, rootY = 100;

// Compute the distinct nodes from the links.
links.forEach(function(link) {
  //console.log(link.source + ":" + link.type);
  if( link.type != null ){
    //At root node
      link.source = nodes[link.source] || (nodes[link.source] = {name: link.source, type: link.type, fixed: true, x: rootX, y: rootY}); 
  }else{
      link.source = nodes[link.source] || (nodes[link.source] = {name: link.source, type: link.type}); 
  }
 
  link.target = nodes[link.target] || (nodes[link.target] = {name: link.target, type: link.type});
});

// testNodes = d3.values(nodes);
// testNodes.forEach(function(tN){
//   console.log("" + tN.name + ":" + tN.type);
// })

var width = 960,
height = 500;

var force = d3.layout.force()
.nodes(d3.values(nodes))
.links(links)
.size([width, height])
.linkDistance(100) //60
.charge(-300)
.on("tick", tick)
.start();

var svg = d3.select("body").append("svg")
.attr("width", width)
.attr("height", height);

// Per-type markers, as they don't inherit styles.
// build the arrow.
svg.append("svg:defs").selectAll("marker")
.data(["end"])
.enter().append("svg:marker")
.attr("id", function(d) { return d; })
.attr("viewBox", "0 -5 10 10")
.attr("refX", 15)
.attr("refY", -1.5)
.attr("markerWidth", 6)
.attr("markerHeight", 6)
.attr("orient", "auto")
.append("svg:path")
.attr("d", "M0,-5L10,0L0,5");

/*  Create the link between nodes */
var path = svg.append("svg:g").selectAll("path")
.data(force.links())
.enter().append("svg:path")
.attr("class", "link")//function(d) { return "link " + d.type; })
.attr("marker-end", "url(#end)");//function(d) { return "url(#" + d.type + ")"; });

// Create the actual nodes */
var circle = svg.append("g").selectAll("circle")
.data(force.nodes())
.enter().append("circle")
.attr("r", 6)//6
// Set the color of the root node to be red so it is noticeable
.style("fill", function (node) { 
  //console.log("in fill. node type is: "+ node.type)
  if(node.name == 'root')
    return '#d62728'; //RED
  if(node.type == 'topic')
    return '#6baed6'; //BLUE
  if(node.type == 'producer')
    return '#d62728'; //'#31a354'; //GREEN
  if(node.type == 'consumer-producer')
    return '#d62728'; //'#31a354'; //GREEN
})
.attr("nodes", function(node){
  //console.log("in new function " + node.name);
  return node;
}) 
.call(force.drag); // This makes the circles draggable

    var text = svg.append("g").selectAll("text")
    .data(force.nodes())
    .enter().append("text")
    .attr("x", 8)
    .attr("y", ".31em")
    .text(function(d) { return d.name; });

// Use elliptical arc path segments to doubly-encode directionality.
function tick() {
  path.attr("d", linkArc);
  circle.attr("transform", transform);
  text.attr("transform", transform);
}

function linkArc(d) {
  var dx = d.target.x - d.source.x,
  dy = d.target.y - d.source.y,
      //dr = Math.sqrt(dx * dx + dy * dy); // CURVED
      dr = 0; // STRAIGHT
      return "M" + d.source.x + "," + d.source.y + "A" + dr + "," + dr + " 0 0,1 " + d.target.x + "," + d.target.y;
    }

    function transform(d) {
      return "translate(" + d.x + "," + d.y + ")";
    }
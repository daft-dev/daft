function shuffle(array) {
  // Based on: http://d3js.org
  var m = array.length, t, i;

  // While there remain elements to shuffle
  while (m) {
    // Pick a remaining element…
    i = Math.floor(Math.random() * m--);

    // And swap it with the current element.
    t = array[m];
    array[m] = array[i];
    array[i] = t;
  }

  return array;
}

function show_examples(image_path, static_path, examples_path, N) {
  fetch(static_path + "/examples.json")
    .then((result) => {
      return result.json();
    })
    .then((json) => {
      var k, nodes = [];
      for (k in json) {
        var node = document.createElement("a");
        node.href = examples_path + "/" + k;
        node.classList.add("example");
        var img = document.createElement("img");
        img.setAttribute("src", image_path + "/" + k + "_2_1.png");
        img.style.objectPosition = `-${json[k][0]}px -${json[k][1]}px`;
        node.appendChild(img);
        nodes.push(node);
      }

      if (typeof (N) !== "undefined")
        nodes = shuffle(nodes).slice(0, N);

      var topNode = document.getElementById("examples-block");
      console.log(topNode);
      nodes.forEach((node) => topNode.appendChild(node));
    })
    .catch((error) => {
      console.error('Error:', error);
    });
}

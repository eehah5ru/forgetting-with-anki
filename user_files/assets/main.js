function getRandomInt(max) {
  return Math.floor(Math.random() * max);
}

function injectEyes(eyePath) {
  $("svg.playImage").replaceWith("<img src='" + eyePath + "'>");

}

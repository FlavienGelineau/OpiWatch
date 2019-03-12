let random = {}

const possibleChar = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
random.string = (length) => {
  let text = "";
  for (let i = 0; i < length; i++) {
    text += possibleChar.charAt(Math.floor(Math.random() * possibleChar.length));
  }
  return text;
}

random.number = (min, max) => {
  return min + Math.random() * (max - min)
}

module.exports = random;
function stepUpValue() {
  const step = parseFloat(this.step) || 1;
  const max = this.max ? parseFloat(this.max) : Number.POSITIVE_INFINITY;
  const value = this.value ? parseFloat(this.value) : 0;
  this.setAttribute("value", Math.min(value + step, max));
}

function stepDownValue() {
  const step = parseFloat(this.step) || 1;
  const min = this.min ? parseFloat(this.min) : Number.NEGATIVE_INFINITY;
  const value = this.value ? parseFloat(this.value) : 0;
  this.setAttribute("value", Math.max(value - step, min));
}

const increaseInputValue = (self) => {
  stepUpValue.call(self.previousElementSibling);
};

const decreaseInputValue = (self) => {
  stepDownValue.call(self.nextElementSibling);
};


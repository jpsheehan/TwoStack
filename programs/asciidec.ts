0[ pushes the top element of the stack as a base 10 encoded string];
{
  $0$ 0[push a zero to the other stack (we will use it to store our string)];
  [
    : 0[copy the number];
    10%48+ 0[get the ascii character of the least significant digit and push it to the ztack];
    `
    10/
  ]$
}~asciidec

12345678
asciidec@
[.;]$
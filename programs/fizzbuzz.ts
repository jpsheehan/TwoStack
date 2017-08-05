{[`]$[.;];$}~p 0[The print function];
$1 1 0[Start at 1];
[
  ;$
  {
    {
      {
        $:`$ 0[Push a copy of the counter];
        $0$[:10%48+`10/]$[`];$ 0[Push the counter as a string];
        $0$10p@ 0[Print the string followed by a newline];
      }
      {;
        0[ print "Buzz" ];
        0$0$"Buzz"10p@
      {}0}

      $:`$ 0[Push a copy of the counter];
      
      5%0=?;@ 0[If the counter is divisible by 5 then execute the top block, else execute the second block.];
    }
    {;
      0[ print "Fizz" ];
      0$0$"Fizz"10p@
    {}0}

    $:`$ 0[Push a copy of the counter];
    
    3%0=?;@ 0[If the counter is disible by 3 then execute the top block, else execute the second block. ];
  }
  {;
    0[ print "Fizzbuzz" ];
    0$0$"Fizzbuzz"10p@
  {}0}

  $:`$: 0[ Push two copies of the counter to the stack ];
  
  3%0=\5%0=&?;@ 0[ if the counter is divisible by 3 and divisible by 5 then execute the top block, else the second block ];
  
  $1+:100< 0[ break the loop if the counter is greater than or equal to 100. ];
]
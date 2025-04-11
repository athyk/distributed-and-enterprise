# Benchmarking

Using Apache benchmark tool, use 

## Posts
```shell
ab -n 1000 -c 50 "http://localhost:8000/posts/list?offset=0&limit=50"
```

Output:
```shell
Document Path:          /posts/list?offset=0&limit=50
Document Length:        19228 bytes

Concurrency Level:      50
Time taken for tests:   124.070 seconds
Complete requests:      1000
Failed requests:        0
Total transferred:      19517000 bytes
HTML transferred:       19228000 bytes
Requests per second:    8.06 [#/sec] (mean)
Time per request:       6203.488 [ms] (mean)
Time per request:       124.070 [ms] (mean, across all concurrent requests)
Transfer rate:          153.62 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.6      0       5
Processing:   395 6036 788.5   6116    6950
Waiting:      395 6034 787.7   6115    6890
Total:        399 6037 788.0   6116    6950

Percentage of the requests served within a certain time (ms)
  50%   6116
  66%   6243
  75%   6316
  80%   6367
  90%   6508
  95%   6648
  98%   6812
  99%   6848
 100%   6950 (longest request)
```

## Degrees

```shell
ab -n 1000 -c 50 "http://localhost:8000/degrees/list/?page=0&limit=50&name=computer"
```

```shell
Concurrency Level:      50
Time taken for tests:   1.463 seconds
Complete requests:      1000
Failed requests:        0
Total transferred:      989000 bytes
HTML transferred:       702000 bytes
Requests per second:    683.43 [#/sec] (mean)
Time per request:       73.160 [ms] (mean)
Time per request:       1.463 [ms] (mean, across all concurrent requests)
Transfer rate:          660.07 [Kbytes/sec] received

Connection Times (ms)
min  mean[+/-sd] median   max
Connect:        0    0   0.4      0       2
Processing:    26   56  27.7     46     351
Waiting:       25   56  27.4     46     325
Total:         28   56  27.9     47     351

Percentage of the requests served within a certain time (ms)
50%     47
66%     49
75%     52
80%     57
90%     95
95%    111
98%    151
99%    172
100%    351 (longest request)
```

## Tags

```shell
ab -n 1000 -c 50 "http://localhost:8000/tags/list/?page=0&limit=50&name=food"
```

```shell
Concurrency Level:      50
Time taken for tests:   0.998 seconds
Complete requests:      1000
Failed requests:        0
Total transferred:      627000 bytes
HTML transferred:       340000 bytes
Requests per second:    1001.93 [#/sec] (mean)
Time per request:       49.904 [ms] (mean)
Time per request:       0.998 [ms] (mean, across all concurrent requests)
Transfer rate:          613.49 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.7      0       6
Processing:    20   45   5.2     44      79
Waiting:       19   45   5.2     44      77
Total:         22   45   5.3     44      80

Percentage of the requests served within a certain time (ms)
  50%     44
  66%     46
  75%     48
  80%     49
  90%     51
  95%     54
  98%     57
  99%     66
 100%     80 (longest request)
```

## Community searching

```shell
Concurrency Level:      50
Time taken for tests:   64.810 seconds
Complete requests:      1000
Failed requests:        0
Total transferred:      5044000 bytes
HTML transferred:       4756000 bytes
Requests per second:    15.43 [#/sec] (mean)
Time per request:       3240.524 [ms] (mean)
Time per request:       64.810 [ms] (mean, across all concurrent requests)
Transfer rate:          76.00 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.5      0       5
Processing:   181 3149 416.5   3181    3724
Waiting:      181 3145 416.4   3174    3724
Total:        185 3149 416.1   3181    3725

Percentage of the requests served within a certain time (ms)
  50%   3181
  66%   3276
  75%   3338
  80%   3378
  90%   3496
  95%   3593
  98%   3634
  99%   3679
 100%   3725 (longest request)
```

## Conclusion
- Community searching is the 2nd slowest
- Posts are the slowest
Some scratches to collect data from FB API.
Posts related data seems to be more interesting.

TODO:
* logging
* exception handling

Also there could be limit of metrics we can get with one request, be careful while adding.

For each posts data is collected just for 100 hours - look into analysis folder why.

For smarter running, try python schedule module

```python
if __name__ == "__main__":
      schedule.every().hour.do(main)
      while True:
          schedule.run_pending()
```
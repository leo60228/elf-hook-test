static const unsigned long long marker = 0x123467890ABCDEFULL;

static int test2;

unsigned long long hook(void) {
  static int test;
  return marker + test;
}

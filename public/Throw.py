class Throw:
    @staticmethod
    def exception(exception, killthread):
        if killthread:
            raise exception
        else:
            try:
                raise exception
            except Exception as e:
                print(e)

if __name__ == "__main__":
    Throw.exception(Exception("Test"), True)
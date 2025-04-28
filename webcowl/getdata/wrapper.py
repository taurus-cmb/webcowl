import asyncio

__all__ = [
    "DataWrapper",
]

class DataWrapper():
    """
    Wrapper around a getdata dirfile, providing the functionality needed for this app
    """

    def __init__(self, dirfile_path=None, fake=False):
        """
        Initialize dirfile wrapper.

        Arguments
        =========
        dirfile_path : str, Path
            The path to the dirfile from which to load data
        fake : bool
            Use fake data instead of reading from dirfile
        """
        if fake:
            self.fake = True
            self.dirfile_path = None
        elif dirfile_path is not None:
            self.fake = False
            self.dirfile_path = dirfile_path
            raise NotImplementedError("TODO handle real dirfiles")
        else:
            raise  ValueError("Must specify one of dirfile_path or fake")
        self.last_index = None
        self.poll_rate = 0.1

    def _read_latest_data_dirfile(self, fields):
        """Read the latest values of data from a dirfile"""
        import pygetdata as gd
        response = dict()
        df = gd.dirfile(self.dirfile_path)
        eof = df.nframes - 1
        response["INDEX"] = eof
        for field in fields:
            # INDEX handled separately
            if field == "INDEX":
                continue
            try:
                response[field] = df.getdata(field, first_frame=eof, num_frames=1)[-1]
            except gd.BadCodeError:
                # leave requests for non-existent fields blank
                continue
        return response

    def _read_latest_data_fake(self, fields):
        """Simulate some fake data for testing, rather than reading from dirfile"""
        from .data_faker import get_fake_data
        return get_fake_data(fields)

    def read_latest_data(self, fields):
        """
        Read the latest values from the dirfile for a list of field names.
        """
        if self.fake:
            result = self._read_latest_data_fake(fields)
        else:
            result = self._read_latest_data_dirfile(fields)
        self.last_index = result["INDEX"]
        return result

    def check_new_data(self):
        """
        Check for the latest value of INDEX in the dirfile
        """
        last_index = self.last_index
        index = self.read_latest_data([])["INDEX"]
        return index != last_index

    async def wait_for_new_data(self, fields):
        """
        Asynchronously wait for new data, then return it
        """
        loop = asyncio.get_running_loop()
        while not await loop.run_in_executor(None, self.check_new_data):
            await asyncio.sleep(self.poll_rate)
        return await loop.run_in_executor(None, self.read_latest_data, fields)

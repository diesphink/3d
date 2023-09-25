import unittest
from build123d import Box
from sphlib import align


class TestAlign(unittest.TestCase):
    def setUp(self):
        self.obj = Box(10, 10, 10)
        self.ref = Box(20, 20, 20)

    def test_begin(self):
        aligned_obj = align(self.obj, self.ref, begin="x", margins=[2, 0, 0])
        self.assertEqual(aligned_obj.bounding_box().min.X, self.ref.bounding_box().min.X + 2)

    def test_array(self):
        aligned_obj = align(self.obj, [0, 0, 0], begin="x", margins=[2, 0, 0])
        self.assertEqual(aligned_obj.bounding_box().min.X, 2)

    # def test_center(self):
    #     aligned_obj = align(self.obj, self.ref, center="y", margins=[0, 2, 0])
    #     self.assertEqual(aligned_obj.bounding_box().mid.y, self.ref.bounding_box().mid.y)

    def test_end(self):
        aligned_obj = align(self.obj, self.ref, end="z", margins=[0, 0, 2])
        self.assertEqual(aligned_obj.bounding_box().max.Z, self.ref.bounding_box().max.Z - 2)

    # def test_beginToEnd(self):
    #     aligned_obj = align(self.obj, self.ref, beginToEnd="y", margin=2)
    #     self.assertEqual(
    #         aligned_obj.bounding_box().min.y, self.ref.bounding_box().max.y - self.obj.bounding_box().size.y - 2
    #     )

    # def test_centerToBegin(self):
    #     aligned_obj = align(self.obj, self.ref, centerToBegin="z", margin=2)
    #     self.assertEqual(
    #         aligned_obj.bounding_box().mid.z, self.ref.bounding_box().min.z + self.obj.bounding_box().size.z / 2 + 2
    #     )

    # def test_endToCenter(self):
    #     aligned_obj = align(self.obj, self.ref, endToCenter="x", margin=2)
    #     self.assertEqual(
    #         aligned_obj.bounding_box().max.x, self.ref.bounding_box().mid.x + self.obj.bounding_box().size.x / 2 - 2
    #     )

    # def test_margins(self):
    #     aligned_obj = align(self.obj, self.ref, center="y", margins=[0, 2, 0])
    #     self.assertEqual(aligned_obj.bounding_box().min.y, self.ref.bounding_box().min.y + 2)
    #     self.assertEqual(aligned_obj.bounding_box().max.y, self.ref.bounding_box().max.y - 2)

    # def test_no_ref(self):
    #     aligned_obj = align(self.obj)
    #     self.assertEqual(aligned_obj.bounding_box().min, self.obj.bounding_box().min)
    #     self.assertEqual(aligned_obj.bounding_box().max, self.obj.bounding_box().max)
    #     self.assertEqual(aligned_obj.bounding_box().mid, self.obj.bounding_box().mid)


if __name__ == "__main__":
    unittest.main()

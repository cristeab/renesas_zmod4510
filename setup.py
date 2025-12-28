from skbuild import setup

setup(
    name="zmod4510",
    version="0.1.0",
    description="ZMOD4510 firmware with Python bindings",
    packages=["zmod4510"],
    cmake_install_dir=".",
    python_requires=">=3.10",
)

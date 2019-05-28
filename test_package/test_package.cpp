#include <spirv-tools/libspirv.hpp>

#include <iostream>

int main()
{
    spvtools::SpirvTools spirvtools(SPV_ENV_VULKAN_1_0);
    std::string s;
    spirvtools.Disassemble({
        0x07230203, // magic number
        0x00010000, // version 1.0.0
        0x00080001, // Khronos Glslang Reference Front End;
        63,         // Bound: 63
        0}, &s);        // Schema: 0
    std::cout << "result of dissassemble:\n" << s << "\n";
    return 0;
}

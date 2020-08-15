#include <windows.h>

//检查当前剪贴板内容是否为图像
__declspec(dllexport) int isImageExists(void)
{

    if (IsClipboardFormatAvailable(CF_DIB))
    {
        return 1;
    }

    else
    {
        return 0;
    }

}


__declspec(dllexport) int saveImage(char* imageSavePath)  // :param: char* imageSavePath  图片保存路径
{

    if (!OpenClipboard(NULL))   // 尝试打开剪贴板
    {
        CloseClipboard(); 
        return 2;              // 打开剪贴板失败
    }

    HANDLE hDib;
    LPVOID lpDib;
    BITMAPFILEHEADER bfBuf;

    //检查剪贴板内容是否为DIB类型的数据
    if (IsClipboardFormatAvailable(CF_DIB))   
    {

        hDib = GetClipboardData(CF_DIB);    // 获取剪贴板内容并
        lpDib = GlobalLock(hDib);           // 得到内存块的首字节指针

        int iData = GlobalSize(lpDib);      

        bfBuf.bfType = 0x4d42;              
        bfBuf.bfReserved1 = 0;
        bfBuf.bfReserved2 = 0;
        
        bfBuf.bfSize = iData + sizeof(BITMAPFILEHEADER);    // 文件大小 = 数据大小 + 文件头大小
        bfBuf.bfOffBits = sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER);  //文件数据写入时的偏移量=文件头大小+信息头大小

        DWORD writ;
        HANDLE hf;

        hf = CreateFileA(imageSavePath, GENERIC_WRITE, 0, NULL, CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL, NULL);
        WriteFile(hf, &bfBuf, sizeof(BITMAPFILEHEADER), &writ, NULL);
        WriteFile(hf, lpDib, iData, &writ, NULL);
        CloseHandle(hf);

        GlobalUnlock(hDib);   // 解锁锁住的内存块
        GlobalFree(hDib);    // 释放内存块
    }

    else
    {
        CloseClipboard();   
        return 1;          // 剪贴板中的内容不是DIB格式
    }

    if (_access(imageSavePath, 0)) 
    {
        CloseClipboard();   
        return 3;          // 路径无法访问 / 没有操作权限
    }

    CloseClipboard();   
    return 0;             // 文件保存成功
}

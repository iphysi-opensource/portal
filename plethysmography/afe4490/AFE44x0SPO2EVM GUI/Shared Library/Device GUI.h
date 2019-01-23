#include "extcode.h"
#pragma pack(push)
#pragma pack(1)

#ifdef __cplusplus
extern "C" {
#endif

void __cdecl GetActiveIDLEWindow(LVBoolean *Write, char ActiveWindowIn[], 
	char GUIName[], char ErrorString[], int32_t *ErrorCode, 
	char ActiveWindowOut[], int32_t len, int32_t len2);
void __cdecl GetScriptFromGUI(uint16_t Method, int32_t TimeoutMs, 
	char DataIn[], char GUIName[], char ErrorString[], int32_t *ErrorCode, 
	LVBoolean *TimedOut, char DataOut[], int32_t len, int32_t len2);
void __cdecl NotifyIDLEClose(char IDLEWindowID[], char GUIName[], 
	char ErrorString[], int32_t *ErrorCode, int32_t len);
void __cdecl NotifyIDLELaunch(char WindowID[], char ResponseNotifier[], 
	char GUIName[], char ErrorString[], int32_t *ErrorCode, int32_t len);
void __cdecl ReadRegister(char RegisterName[], char BlockName[], 
	char GUIName[], char ErrorString[], int32_t *ErrorCode, uint64_t *LastRead, 
	int32_t len);
void __cdecl WriteRegister(uint64_t Data, char RegisterName[], 
	char BlockName[], char GUIName[], char ErrorString[], int32_t *ErrorCode, 
	LVBoolean *Complete, int32_t len);

long __cdecl LVDLLStatus(char *errStr, int errStrLen, void *module);

#ifdef __cplusplus
} // extern "C"
#endif

#pragma pack(pop)


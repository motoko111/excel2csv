
#include "Master/MasterDataSubsystem.h"

UMasterDataSubsystem* UMasterDataSubsystem::GetInstance()
{
	if (!GEngine || !GEngine->GameViewport) return nullptr;
	UGameInstance* _GameInst = GEngine->GameViewport->GetWorld()->GetGameInstance();
	return _GameInst->GetSubsystem<UMasterDataSubsystem>();
}

void UMasterDataSubsystem::Initialize(FSubsystemCollectionBase& Collection)
{
	FString fileName = GetFileName();
	if (fileName.IsEmpty()) return;

	FString dataTablePath = FString::Printf(TEXT("/Game/Master/%s.%s"), *fileName, *fileName);
	dataTable = LoadObject<UDataTable>(nullptr, *dataTablePath, nullptr, LOAD_None, nullptr);
}

void UMasterDataSubsystem::Deinitialize()
{
}

UDataTable* UMasterDataSubsystem::GetDataTable()
{
	return dataTable;
}
#pragma once

#include "CoreMinimal.h"
#include "Engine/DataTable.h"
#include "Master/MasterDataSubsystem.h"
#include "${DATA_NAME}Manager.generated.h"

USTRUCT(BlueprintType)
struct F${DATA_NAME} : public FTableRowBase
{
	GENERATED_BODY()
	
public:
${FIELDS}
};

UCLASS()
class U${DATA_NAME}Manager : public UMasterDataSubsystem
{
	GENERATED_BODY()

protected:
	virtual FString GetFileName() override { return TEXT("${DATA_NAME}"); }
};
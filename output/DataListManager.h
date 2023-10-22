#pragma once

#include "CoreMinimal.h"
#include "Engine/DataTable.h"
#include "Master/MasterDataSubsystem.h"
#include "Master/Data/MasterDefines.h"
#include "DataListManager.generated.h"

USTRUCT(BlueprintType)
struct FDataList : public FTableRowBase
{
	GENERATED_BODY()
	
public:
	UPROPERTY(EditAnywhere)
	FName Id;
	UPROPERTY(EditAnywhere)
	FString Name;
	UPROPERTY(EditAnywhere)
	FString Text;
	UPROPERTY(EditAnywhere)
	int IntValue;
	UPROPERTY(EditAnywhere)
	float FloatValue;
	UPROPERTY(EditAnywhere)
	double DoubleValue;

};

UCLASS()
class UDataListManager : public UMasterDataSubsystem
{
	GENERATED_BODY()

protected:
	virtual FString GetFileName() override { return TEXT("DataList"); }
};
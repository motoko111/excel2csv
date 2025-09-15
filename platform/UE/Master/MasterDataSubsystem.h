// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Subsystems/GameInstanceSubsystem.h"
#include "Engine/DataTable.h"
#include "MasterDataSubsystem.generated.h"

/**
 *
 */
UCLASS()
class LUASAMPLE_API UMasterDataSubsystem : public UGameInstanceSubsystem
{
	GENERATED_BODY()
public:
	virtual void Initialize(FSubsystemCollectionBase& Collection) override;
	virtual void Deinitialize() override;
public:
	static UMasterDataSubsystem* GetInstance();

	UDataTable* GetDataTable();

	template<typename T>
	const T* GetData(const FName id) const
	{
		if (IsValid(dataTable))
		{
			return dataTable->FindRow(id);
		}
		return nullptr;
	}

protected:
	virtual FString GetFileName() { return TEXT(""); }

private:
	UPROPERTY()
	UDataTable* dataTable;
};

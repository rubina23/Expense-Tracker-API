from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
import models, schemas
from database import get_db
from router.auth import get_current_user  

router = APIRouter(prefix="/transactions", tags=["Transactions"])

# ==========================
# 1. Create Transaction
# ==========================
@router.post("/", response_model=schemas.TransactionResponse, status_code=status.HTTP_201_CREATED)
def create_transaction(
    transaction: schemas.TransactionCreate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    # Assign logged-in user as transaction owner
    new_transaction = models.Transaction(
        **transaction.model_dump(), 
        owner_id=current_user.id
    )
    # Save to the database
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    return new_transaction 

# ==========================
# Transaction Filtering 
# ==========================
@router.get("/filter", response_model=List[schemas.TransactionResponse])
def filter_transactions(
    type: Optional[str] = Query(None, description="expense or income"),
    category: Optional[str] = Query(None),
    minimum_amount: Optional[float] = Query(None),
    maximum_amount: Optional[float] = Query(None),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Filter transactions for the logged-in user 
    query = db.query(models.Transaction).filter(models.Transaction.owner_id == current_user.id)
    
    if type:
        query = query.filter(models.Transaction.type == type)
    if category:
        query = query.filter(models.Transaction.category == category)
    if minimum_amount is not None:
        query = query.filter(models.Transaction.amount >= minimum_amount)
    if maximum_amount is not None:
        query = query.filter(models.Transaction.amount <= maximum_amount)
        
    return query.all()

# ==========================
# 2. Get All Transactions
# ==========================
@router.get("/", response_model=List[schemas.TransactionResponse])
def get_all_transactions(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    # Return transactions only for the logged-in user 
    return db.query(models.Transaction).filter(models.Transaction.owner_id == current_user.id).all()

# ==========================
# 3. Get Transaction By ID
# ==========================
@router.get("/{transaction_id}", response_model=schemas.TransactionResponse)
def get_transaction(transaction_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    transaction = db.query(models.Transaction).filter(
        models.Transaction.id == transaction_id, 
        models.Transaction.owner_id == current_user.id # Prevent access to other users' transactions
    ).first()
    
    if not transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    return transaction # Return a specific transaction

# ==========================
# 4. Update Transaction
# ==========================
@router.put("/{transaction_id}", response_model=schemas.TransactionResponse)
def update_transaction(
    transaction_id: int, 
    updated_tran: schemas.TransactionCreate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    transaction_query = db.query(models.Transaction).filter(
        models.Transaction.id == transaction_id, 
        models.Transaction.owner_id == current_user.id # Allow users to update only their own transactions
    )
    transaction = transaction_query.first()
    
    if not transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found") 
        
    transaction_query.update(updated_tran.model_dump(), synchronize_session=False)
    db.commit()

    # Return the updated transaction
    return transaction_query.first() 

# ==========================
# 5. Delete Transaction
# ==========================
@router.delete("/{transaction_id}", status_code=status.HTTP_200_OK)
def delete_transaction(transaction_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    transaction_query = db.query(models.Transaction).filter(
        models.Transaction.id == transaction_id, 
        models.Transaction.owner_id == current_user.id
    )
    transaction = transaction_query.first()
    
    if not transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found") 
        
    transaction_query.delete(synchronize_session=False) # Delete from DB
    db.commit()
    
    return {"message": "Transaction deleted successfully"} 

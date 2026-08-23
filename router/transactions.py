from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
import models, schemas
from database import get_db
from router.auth import get_current_user  # get_current_user ইমপোর্ট করা হলো

router = APIRouter(prefix="/transactions", tags=["Transactions"])

# ==========================
# 1. Create Transaction[cite: 1]
# ==========================
@router.post("/", response_model=schemas.TransactionResponse, status_code=status.HTTP_201_CREATED)
def create_transaction(
    transaction: schemas.TransactionCreate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    # লগ-ইন করা ইউজারকে ট্রানজেকশনের ওনার হিসেবে এসাইন করা[cite: 1]
    new_transaction = models.Transaction(
        **transaction.model_dump(), 
        owner_id=current_user.id
    )
    # ডেটাবেসে সেভ করা[cite: 1]
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    return new_transaction # তৈরি করা ট্রানজেকশন রিটার্ন করা[cite: 1]

# ==========================
# Transaction Filtering (15 Marks) - এটা GET অল এর আগেই লিখতে হবে, না হলে FastAPI আইডি হিসেবে কাউন্ট করতে পারে[cite: 1]
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
    # শুধুমাত্র লগ-ইন করা ইউজারের ট্রানজেকশনগুলো ফিল্টার করা[cite: 1]
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
# 2. Get All Transactions[cite: 1]
# ==========================
@router.get("/", response_model=List[schemas.TransactionResponse])
def get_all_transactions(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    # শুধুমাত্র লগ-ইন করা ইউজারের ট্রানজেকশন রিটার্ন করা[cite: 1]
    return db.query(models.Transaction).filter(models.Transaction.owner_id == current_user.id).all()

# ==========================
# 3. Get Transaction By ID[cite: 1]
# ==========================
@router.get("/{transaction_id}", response_model=schemas.TransactionResponse)
def get_transaction(transaction_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    transaction = db.query(models.Transaction).filter(
        models.Transaction.id == transaction_id, 
        models.Transaction.owner_id == current_user.id # অন্য ইউজারের ট্রানজেকশন এক্সেস বন্ধ করা[cite: 1]
    ).first()
    
    if not transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found") # 404 এরর[cite: 1]
    return transaction # নির্দিষ্ট ট্রানজেকশন রিটার্ন করা[cite: 1]

# ==========================
# 4. Update Transaction[cite: 1]
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
        models.Transaction.owner_id == current_user.id # ইউজার শুধুমাত্র নিজের ট্রানজেকশন আপডেট করতে পারবে[cite: 1]
    )
    transaction = transaction_query.first()
    
    if not transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found") # 404 এরর, ক্র্যাশ করবে না[cite: 1]
        
    transaction_query.update(updated_tran.model_dump(), synchronize_session=False)
    db.commit()
    # আপডেট করা ট্রানজেকশন রিটার্ন করা[cite: 1]
    return transaction_query.first() 

# ==========================
# 5. Delete Transaction[cite: 1]
# ==========================
@router.delete("/{transaction_id}", status_code=status.HTTP_200_OK)
def delete_transaction(transaction_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    transaction_query = db.query(models.Transaction).filter(
        models.Transaction.id == transaction_id, 
        models.Transaction.owner_id == current_user.id
    )
    transaction = transaction_query.first()
    
    if not transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found") # 404 এরর, ক্র্যাশ করবে না[cite: 1]
        
    transaction_query.delete(synchronize_session=False) # ডেটাবেস থেকে ডিলিট করা[cite: 1]
    db.commit()
    
    return {"message": "Transaction deleted successfully"} # কনফার্মেশন মেসেজ রিটার্ন করা[cite: 1]
@router.post("/verify")
async def telegram_verify(request: Request):
    body = await request.json()
    init_data = body.get("initData")
    data = verify_telegram_auth(parse_init_data(init_data))  # sizning verify qismi

    telegram_id = data["id"]
    # DB bilan qidirish: telegram_id maydoni bo'lishi kerak modelda
    user = db.query(User).filter(User.telegram_id == telegram_id).first()

    if not user:
        # agar logged in JWT mavjud va biz link qilishni xohlasak:
        current_user = get_current_user_from_header(request)
        if current_user:
            current_user.telegram_id = telegram_id
            db.commit()
            user = current_user
        else:
            # yangi user yaratish
            user = User(first_name=data.get("first_name"), telegram_id=telegram_id)
            db.add(user)
            db.commit()
            db.refresh(user)

    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "user": user_to_dict(user)}
